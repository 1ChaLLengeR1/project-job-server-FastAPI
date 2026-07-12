from dataclasses import dataclass, field
from datetime import date, datetime

from database.psql.models.rentals import (
    RentalBillingPeriod,
    RentalMeterReading,
    RentalSettlement,
    RentalSettlementItem,
)


@dataclass
class BillingPeriodResponse:
    id: str
    period_month: date
    status: str
    electricity_bill_amount: float | None
    electricity_rate: float | None
    electricity_rate_is_manual: bool
    water_rate: float
    note: str | None
    created_at: datetime | None
    updated_at: datetime | None


@dataclass
class MeterReadingResponse:
    id: str
    period_id: str
    meter_id: str
    previous_value: float
    current_value: float
    error_correction: float
    created_at: datetime | None
    updated_at: datetime | None


@dataclass
class SettlementItemResponse:
    id: str
    settlement_id: str
    cost_type_id: str | None
    name: str
    kind: str
    amount: float
    created_at: datetime | None
    updated_at: datetime | None


@dataclass
class SettlementResponse:
    id: str
    period_id: str
    apartment_id: str
    tenancy_id: str | None
    rent_amount: float
    electricity_consumption: float
    electricity_cost: float
    water_consumption: float
    water_cost: float
    total_media_amount: float
    total_amount: float
    note: str | None
    created_at: datetime | None
    updated_at: datetime | None
    items: list[SettlementItemResponse] = field(default_factory=list)


@dataclass
class SettlementItemInput:
    """Dane wejściowe pozycji rozliczenia (koszt stały / korekta) przy tworzeniu snapshotu."""

    name: str
    kind: str  # fixed_cost | adjustment
    amount: float
    cost_type_id: str | None = None


def _to_billing_period_response(model: RentalBillingPeriod) -> BillingPeriodResponse:
    return BillingPeriodResponse(
        id=str(model.id),
        period_month=model.period_month,
        status=model.status,
        electricity_bill_amount=float(model.electricity_bill_amount)
        if model.electricity_bill_amount is not None
        else None,
        electricity_rate=float(model.electricity_rate) if model.electricity_rate is not None else None,
        electricity_rate_is_manual=model.electricity_rate_is_manual,
        water_rate=float(model.water_rate),
        note=model.note,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def _to_meter_reading_response(model: RentalMeterReading) -> MeterReadingResponse:
    return MeterReadingResponse(
        id=str(model.id),
        period_id=str(model.period_id),
        meter_id=str(model.meter_id),
        previous_value=float(model.previous_value),
        current_value=float(model.current_value),
        error_correction=float(model.error_correction),
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def _to_settlement_item_response(model: RentalSettlementItem) -> SettlementItemResponse:
    return SettlementItemResponse(
        id=str(model.id),
        settlement_id=str(model.settlement_id),
        cost_type_id=str(model.cost_type_id) if model.cost_type_id else None,
        name=model.name,
        kind=model.kind,
        amount=float(model.amount),
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def _to_settlement_response(
    model: RentalSettlement, items: list[RentalSettlementItem] | None = None
) -> SettlementResponse:
    return SettlementResponse(
        id=str(model.id),
        period_id=str(model.period_id),
        apartment_id=str(model.apartment_id),
        tenancy_id=str(model.tenancy_id) if model.tenancy_id else None,
        rent_amount=float(model.rent_amount),
        electricity_consumption=float(model.electricity_consumption),
        electricity_cost=float(model.electricity_cost),
        water_consumption=float(model.water_consumption),
        water_cost=float(model.water_cost),
        total_media_amount=float(model.total_media_amount),
        total_amount=float(model.total_amount),
        note=model.note,
        created_at=model.created_at,
        updated_at=model.updated_at,
        items=[_to_settlement_item_response(item) for item in (items or [])],
    )
