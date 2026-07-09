from decimal import ROUND_HALF_UP, Decimal

from api.response import ApiErrorData
from core.service.rental.billing.response import (
    AdjustmentInput,
    ApartmentCostInput,
    ApartmentSettlementResponse,
    MediaCostResponse,
    SettlementItemCalcResponse,
)


def _round_full_zl(value: float) -> float:
    """Zaokrąglenie do pełnych złotych half-up — odpowiednik "~" z ręcznych obliczeń."""
    return float(Decimal(str(value)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def _round_grosze(value: float) -> float:
    return float(Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def calculation_media_cost(
    consumption: float, rate: float
) -> tuple[MediaCostResponse | None, ApiErrorData | None, bool]:
    """Koszt medium: zużycie x stawka, zaokrąglone do pełnych złotych."""
    try:
        if consumption < 0:
            return (
                None,
                ApiErrorData(
                    message=f"Ujemne zużycie: {consumption}",
                    type_module="calculation_media_cost",
                    type_error="exception",
                    key_type_error="Exception",
                ),
                False,
            )
        if rate < 0:
            return (
                None,
                ApiErrorData(
                    message=f"Ujemna stawka: {rate}",
                    type_module="calculation_media_cost",
                    type_error="exception",
                    key_type_error="Exception",
                ),
                False,
            )

        cost = _round_full_zl(consumption * rate)
        return MediaCostResponse(consumption=consumption, rate=rate, cost=cost), None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="calculation_media_cost",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def calculation_fixed_costs(
    costs: list[ApartmentCostInput], persons_count: int
) -> tuple[list[SettlementItemCalcResponse] | None, ApiErrorData | None, bool]:
    """Wycena kosztów stałych mieszkania: fixed = kwota, per_person = stawka x liczba osób."""
    try:
        if persons_count < 1:
            return (
                None,
                ApiErrorData(
                    message=f"Liczba osób musi być co najmniej 1, otrzymano: {persons_count}",
                    type_module="calculation_fixed_costs",
                    type_error="exception",
                    key_type_error="Exception",
                ),
                False,
            )

        items = []
        for cost in costs:
            if cost.charge_type == "fixed":
                name = cost.name
                amount = _round_grosze(cost.amount)
            elif cost.charge_type == "per_person":
                name = f"{cost.name} ({persons_count} os. x {cost.amount} zł)"
                amount = _round_grosze(cost.amount * persons_count)
            else:
                return (
                    None,
                    ApiErrorData(
                        message=f"Nieznany typ naliczania kosztu: '{cost.charge_type}' ({cost.name})",
                        type_module="calculation_fixed_costs",
                        type_error="exception",
                        key_type_error="Exception",
                    ),
                    False,
                )

            items.append(
                SettlementItemCalcResponse(
                    name=name,
                    kind="fixed_cost",
                    amount=amount,
                    cost_type_id=cost.cost_type_id,
                )
            )
        return items, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="calculation_fixed_costs",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def calculation_apartment_settlement(
    apartment_id: str,
    electricity_consumption: float,
    electricity_rate: float,
    water_consumption: float,
    water_rate: float,
    fixed_costs: list[ApartmentCostInput],
    adjustments: list[AdjustmentInput],
    tenancy_id: str | None = None,
    rent_amount: float = 0.0,
    persons_count: int = 1,
) -> tuple[ApartmentSettlementResponse | None, ApiErrorData | None, bool]:
    """Pełne rozliczenie mieszkania w okresie: media + koszty stałe + korekty (+ czynsz).

    Odpowiednik sekcji per mieszkanie z ręcznych obliczeń:
    Prąd + Woda + Śmieci + Internet + ... + korekty = "Razem" (total_media_amount).
    """
    try:
        electricity, error, ok = calculation_media_cost(electricity_consumption, electricity_rate)
        if not ok:
            return None, error, False

        water, error, ok = calculation_media_cost(water_consumption, water_rate)
        if not ok:
            return None, error, False

        fixed_items, error, ok = calculation_fixed_costs(fixed_costs, persons_count)
        if not ok:
            return None, error, False

        adjustment_items = [
            SettlementItemCalcResponse(
                name=adjustment.name,
                kind="adjustment",
                amount=_round_grosze(adjustment.amount),
            )
            for adjustment in adjustments
        ]

        items = fixed_items + adjustment_items
        total_media_amount = _round_grosze(electricity.cost + water.cost + sum(item.amount for item in items))
        total_amount = _round_grosze(total_media_amount + rent_amount)

        return (
            ApartmentSettlementResponse(
                apartment_id=apartment_id,
                tenancy_id=tenancy_id,
                rent_amount=_round_grosze(rent_amount),
                electricity_consumption=electricity_consumption,
                electricity_cost=electricity.cost,
                water_consumption=water_consumption,
                water_cost=water.cost,
                total_media_amount=total_media_amount,
                total_amount=total_amount,
                items=items,
            ),
            None,
            True,
        )
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="calculation_apartment_settlement",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
