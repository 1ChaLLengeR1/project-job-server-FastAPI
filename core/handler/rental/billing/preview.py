from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.handler.rental.billing.response import (
    PeriodAdjustmentInput,
    PeriodBeneficiaryPreview,
    PeriodPreviewResponse,
    PeriodSettlementPreview,
)
from core.repository.psql.logs.create import create_logs_psql
from core.repository.psql.rental.billing.collection import collection_meter_readings_psql
from core.repository.psql.rental.billing.one import one_billing_period_psql
from core.repository.psql.rental.dictionaries.collection import (
    collection_apartment_costs_psql,
    collection_apartments_psql,
    collection_cost_types_psql,
    collection_meters_psql,
    collection_tenancies_psql,
)
from core.repository.psql.rental.family.collection import (
    collection_allocation_rules_psql,
    collection_beneficiaries_psql,
)
from core.service.rental.billing.calculation import calculation_apartment_settlement
from core.service.rental.billing.response import AdjustmentInput, ApartmentCostInput
from core.service.rental.family.calculation import calculation_family_allocation
from core.service.rental.family.response import (
    AllocationRuleInput,
    AllocationSettlementInput,
    AllocationSettlementItemInput,
)
from core.service.rental.meters.calculation import (
    calculation_electricity_rate,
    calculation_main_meter_error,
    calculation_meter_consumptions,
)
from core.service.rental.meters.response import MeterReadingInput


def _compute_period(
    period_id: str,
    adjustments: list[PeriodAdjustmentInput] | None = None,
    settlement_ids: dict[str, str] | None = None,
    db_session: Session | None = None,
) -> tuple[PeriodPreviewResponse | None, ApiErrorData | None, bool]:
    """Pełne wyliczenie okresu — wspólne dla preview i close.

    settlement_ids: mapa apartment_id -> settlement_id (przy close podpina pozycje
    podziału rodzinnego do zapisanych snapshotów; przy preview None).
    """
    adjustments = adjustments or []
    settlement_ids = settlement_ids or {}
    warnings: list[str] = []

    period, err, ok = one_billing_period_psql(period_id, db_session=db_session)
    if not ok:
        return None, err, False

    readings, err, ok = collection_meter_readings_psql(period_id, db_session=db_session)
    if not ok:
        return None, err, False

    meters, err, ok = collection_meters_psql(db_session=db_session)
    if not ok:
        return None, err, False
    meters_by_id = {meter.id: meter for meter in meters}

    reading_inputs = []
    for reading in readings:
        meter = meters_by_id.get(reading.meter_id)
        if not meter:
            return (
                None,
                ApiErrorData(
                    message=f"Licznik odczytu nie istnieje: {reading.meter_id}",
                    type_module="_compute_period",
                    type_error="not_found",
                    key_type_error="NotFound",
                ),
                False,
            )
        reading_inputs.append(
            MeterReadingInput(
                meter_id=meter.id,
                apartment_id=meter.apartment_id,
                media_type=meter.media_type,
                is_master=meter.is_master,
                previous_value=reading.previous_value,
                current_value=reading.current_value,
                error_correction=reading.error_correction,
            )
        )

    consumptions, err, ok = calculation_meter_consumptions(reading_inputs)
    if not ok:
        return None, err, False

    electricity_apartments = [
        consumption
        for consumption in consumptions
        if consumption.apartment_id is not None and consumption.media_type == "electricity"
    ]
    total_kwh = round(sum(consumption.consumption for consumption in electricity_apartments), 3)

    # stawka prądu: ręczna ma priorytet, potem wyliczana z rachunku, potem zapisana w okresie
    if period.electricity_rate_is_manual and period.electricity_rate is not None:
        electricity_rate = period.electricity_rate
    elif period.electricity_bill_amount is not None and total_kwh > 0:
        rate_result, err, ok = calculation_electricity_rate(period.electricity_bill_amount, total_kwh)
        if not ok:
            return None, err, False
        electricity_rate = rate_result.rate
    elif period.electricity_rate is not None:
        electricity_rate = period.electricity_rate
    else:
        electricity_rate = 0.0
        if total_kwh > 0:
            warnings.append("Brak stawki prądu — podaj kwotę rachunku lub stawkę ręczną")

    # błąd licznika głównego (tylko gdy w okresie jest odczyt licznika głównego prądu)
    main_meter_error = None
    main_consumption = next(
        (
            consumption
            for consumption in consumptions
            if consumption.apartment_id is None and consumption.media_type == "electricity"
        ),
        None,
    )
    if main_consumption:
        main_meter_error, err, ok = calculation_main_meter_error(
            main_consumption.raw_difference, electricity_apartments
        )
        if not ok:
            return None, err, False

    apartments, err, ok = collection_apartments_psql(db_session=db_session)
    if not ok:
        return None, err, False

    cost_types, err, ok = collection_cost_types_psql(db_session=db_session)
    if not ok:
        return None, err, False
    cost_types_by_id = {cost_type.id: cost_type for cost_type in cost_types}

    consumption_by_apartment: dict[tuple[str, str], float] = {}
    for consumption in consumptions:
        if consumption.apartment_id is None:
            continue
        key = (consumption.apartment_id, consumption.media_type)
        consumption_by_apartment[key] = consumption_by_apartment.get(key, 0) + consumption.consumption

    period_day = period.period_month
    settlement_previews: list[PeriodSettlementPreview] = []
    for apartment in apartments:
        tenancies, err, ok = collection_tenancies_psql(
            apartment_id=apartment.id, active_on=period_day, db_session=db_session
        )
        if not ok:
            return None, err, False

        costs, err, ok = collection_apartment_costs_psql(
            apartment_id=apartment.id, active_on=period_day, db_session=db_session
        )
        if not ok:
            return None, err, False

        electricity = consumption_by_apartment.get((apartment.id, "electricity"))
        water = consumption_by_apartment.get((apartment.id, "water"))
        apartment_adjustments = [
            AdjustmentInput(name=adjustment.name, amount=adjustment.amount)
            for adjustment in adjustments
            if adjustment.apartment_id == apartment.id
        ]

        # mieszkanie bez najmu, kosztów, odczytów i korekt w tym okresie — pomijamy
        if not tenancies and not costs and electricity is None and water is None and not apartment_adjustments:
            continue

        if len(tenancies) > 1:
            warnings.append(f"Mieszkanie '{apartment.name}': więcej niż jeden najem aktywny w tym okresie")
        tenancy = tenancies[0] if tenancies else None

        fixed_costs = []
        for cost in costs:
            cost_type = cost_types_by_id.get(cost.cost_type_id)
            if not cost_type:
                return (
                    None,
                    ApiErrorData(
                        message=f"Rodzaj kosztu nie istnieje: {cost.cost_type_id}",
                        type_module="_compute_period",
                        type_error="not_found",
                        key_type_error="NotFound",
                    ),
                    False,
                )
            fixed_costs.append(
                ApartmentCostInput(
                    cost_type_id=cost_type.id,
                    name=cost_type.name,
                    charge_type=cost_type.charge_type,
                    amount=cost.amount,
                )
            )

        settlement, err, ok = calculation_apartment_settlement(
            apartment_id=apartment.id,
            electricity_consumption=electricity or 0,
            electricity_rate=electricity_rate,
            water_consumption=water or 0,
            water_rate=period.water_rate,
            fixed_costs=fixed_costs,
            adjustments=apartment_adjustments,
            tenancy_id=tenancy.id if tenancy else None,
            rent_amount=tenancy.rent_amount if tenancy else 0,
            persons_count=tenancy.persons_count if tenancy else 1,
        )
        if not ok:
            return None, err, False

        settlement_previews.append(
            PeriodSettlementPreview(apartment_id=apartment.id, apartment_name=apartment.name, settlement=settlement)
        )

    # podział rodzinny wg reguł aktywnych w miesiącu okresu
    rules, err, ok = collection_allocation_rules_psql(active_on=period_day, db_session=db_session)
    if not ok:
        return None, err, False

    rule_inputs = [
        AllocationRuleInput(
            rule_id=rule.id,
            beneficiary_id=rule.beneficiary_id,
            component=rule.component,
            mode=rule.mode,
            apartment_id=rule.apartment_id,
            cost_type_id=rule.cost_type_id,
            amount=rule.amount,
            description=rule.description,
        )
        for rule in rules
    ]
    allocation_settlements = [
        AllocationSettlementInput(
            apartment_id=preview.apartment_id,
            apartment_name=preview.apartment_name,
            rent_amount=preview.settlement.rent_amount,
            electricity_cost=preview.settlement.electricity_cost,
            water_cost=preview.settlement.water_cost,
            settlement_id=settlement_ids.get(preview.apartment_id),
            items=[
                AllocationSettlementItemInput(
                    name=item.name, kind=item.kind, amount=item.amount, cost_type_id=item.cost_type_id
                )
                for item in preview.settlement.items
            ],
        )
        for preview in settlement_previews
    ]

    family, err, ok = calculation_family_allocation(rule_inputs, allocation_settlements)
    if not ok:
        return None, err, False
    warnings.extend(family.warnings)

    beneficiaries, err, ok = collection_beneficiaries_psql(db_session=db_session)
    if not ok:
        return None, err, False
    beneficiary_names = {beneficiary.id: beneficiary.name for beneficiary in beneficiaries}

    beneficiary_previews = [
        PeriodBeneficiaryPreview(
            beneficiary_id=allocation.beneficiary_id,
            beneficiary_name=beneficiary_names.get(allocation.beneficiary_id, allocation.beneficiary_id),
            total_amount=allocation.total_amount,
            items=allocation.items,
        )
        for allocation in family.beneficiaries
    ]

    return (
        PeriodPreviewResponse(
            period=period,
            electricity_rate=electricity_rate,
            electricity_total_consumption=total_kwh,
            main_meter_error=main_meter_error,
            consumptions=consumptions,
            settlements=settlement_previews,
            beneficiaries=beneficiary_previews,
            warnings=warnings,
        ),
        None,
        True,
    )


def handler_preview_billing_period(
    user_id: str,
    period_id: str,
    adjustments: list[PeriodAdjustmentInput] | None = None,
    db_session: Session | None = None,
) -> tuple[PeriodPreviewResponse | None, ApiErrorData | None, bool]:
    """Wyliczenie okresu na żywo — nic nie zapisuje."""
    try:
        result, err, ok = _compute_period(period_id, adjustments, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:preview_billing_period", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_preview_billing_period",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
