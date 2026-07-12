from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.handler.rental.billing.preview import _compute_period
from core.handler.rental.billing.response import PeriodAdjustmentInput, PeriodPreviewResponse
from core.repository.psql.logs.create import create_logs_psql
from core.repository.psql.rental.billing.create import create_settlement_psql
from core.repository.psql.rental.billing.delete import delete_settlements_by_period_psql
from core.repository.psql.rental.billing.one import one_billing_period_psql
from core.repository.psql.rental.billing.response import BillingPeriodResponse, SettlementItemInput
from core.repository.psql.rental.billing.update import (
    update_billing_period_psql,
    update_billing_period_status_psql,
)
from core.repository.psql.rental.family.create import create_beneficiary_settlement_psql
from core.repository.psql.rental.family.response import BeneficiarySettlementItemInput


def handler_close_billing_period(
    user_id: str,
    period_id: str,
    adjustments: list[PeriodAdjustmentInput] | None = None,
    db_session: Session | None = None,
) -> tuple[PeriodPreviewResponse | None, ApiErrorData | None, bool]:
    """Zamknięcie okresu: wyliczenie + zapis snapshotów (rozliczenia mieszkań i podział rodzinny).

    Zamknięty okres nie zmienia się przy późniejszej edycji słowników — kwoty są skopiowane.
    """
    try:
        period, err, ok = one_billing_period_psql(period_id, db_session=db_session)
        if not ok:
            return None, err, False
        if period.status == "closed":
            return (
                None,
                ApiErrorData(
                    message="Okres jest już zamknięty",
                    type_module="handler_close_billing_period",
                    type_error="integrity_error",
                    key_type_error="IntegrityError",
                ),
                False,
            )

        preview, err, ok = _compute_period(period_id, adjustments, db_session=db_session)
        if not ok:
            return None, err, False

        # snapshot rozliczeń mieszkań
        settlement_ids: dict[str, str] = {}
        for settlement_preview in preview.settlements:
            settlement = settlement_preview.settlement
            created, err, ok = create_settlement_psql(
                period_id=period_id,
                apartment_id=settlement_preview.apartment_id,
                tenancy_id=settlement.tenancy_id,
                rent_amount=settlement.rent_amount,
                electricity_consumption=settlement.electricity_consumption,
                electricity_cost=settlement.electricity_cost,
                water_consumption=settlement.water_consumption,
                water_cost=settlement.water_cost,
                total_media_amount=settlement.total_media_amount,
                total_amount=settlement.total_amount,
                items=[
                    SettlementItemInput(
                        name=item.name, kind=item.kind, amount=item.amount, cost_type_id=item.cost_type_id
                    )
                    for item in settlement.items
                ],
                db_session=db_session,
            )
            if not ok:
                return None, err, False
            settlement_ids[settlement_preview.apartment_id] = created.id

        # ponowne wyliczenie podziału z podpiętymi id snapshotów + zapis
        final_preview, err, ok = _compute_period(
            period_id, adjustments, settlement_ids=settlement_ids, db_session=db_session
        )
        if not ok:
            return None, err, False

        for beneficiary in final_preview.beneficiaries:
            _, err, ok = create_beneficiary_settlement_psql(
                period_id,
                beneficiary.beneficiary_id,
                beneficiary.total_amount,
                items=[
                    BeneficiarySettlementItemInput(
                        description=item.description,
                        amount=item.amount,
                        rule_id=item.rule_id,
                        settlement_id=item.settlement_id,
                    )
                    for item in beneficiary.items
                ],
                db_session=db_session,
            )
            if not ok:
                return None, err, False

        # utrwalenie użytej stawki prądu w okresie + zamknięcie
        _, err, ok = update_billing_period_psql(
            period_id,
            period.electricity_bill_amount,
            final_preview.electricity_rate,
            period.electricity_rate_is_manual,
            period.water_rate,
            period.note,
            db_session=db_session,
        )
        if not ok:
            return None, err, False

        closed_period, err, ok = update_billing_period_status_psql(period_id, "closed", db_session=db_session)
        if not ok:
            return None, err, False
        final_preview.period = closed_period

        create_logs_psql(user_id, "rental:close_billing_period", db_session=db_session)
        return final_preview, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_close_billing_period",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def handler_reopen_billing_period(
    user_id: str, period_id: str, db_session: Session | None = None
) -> tuple[BillingPeriodResponse | None, ApiErrorData | None, bool]:
    """Ponowne otwarcie okresu: kasuje snapshoty, zostawia odczyty i dane wejściowe."""
    try:
        period, err, ok = one_billing_period_psql(period_id, db_session=db_session)
        if not ok:
            return None, err, False
        if period.status != "closed":
            return (
                None,
                ApiErrorData(
                    message="Okres nie jest zamknięty",
                    type_module="handler_reopen_billing_period",
                    type_error="integrity_error",
                    key_type_error="IntegrityError",
                ),
                False,
            )

        _, err, ok = delete_settlements_by_period_psql(period_id, db_session=db_session)
        if not ok:
            return None, err, False

        reopened_period, err, ok = update_billing_period_status_psql(period_id, "draft", db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:reopen_billing_period", db_session=db_session)
        return reopened_period, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_reopen_billing_period",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
