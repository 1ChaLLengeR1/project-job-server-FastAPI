from datetime import date

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.rental.billing.response import (
    BillingPeriodResponse,
    MeterReadingResponse,
    SettlementItemInput,
    SettlementResponse,
    _to_billing_period_response,
    _to_meter_reading_response,
    _to_settlement_response,
)
from database.psql.database import managed_session
from database.psql.models.rentals import (
    RentalBillingPeriod,
    RentalMeterReading,
    RentalSettlement,
    RentalSettlementItem,
)


def create_billing_period_psql(
    period_month: date,
    electricity_bill_amount: float | None = None,
    electricity_rate: float | None = None,
    electricity_rate_is_manual: bool = False,
    water_rate: float = 9.00,
    note: str | None = None,
    db_session: Session | None = None,
) -> tuple[BillingPeriodResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            new_period = RentalBillingPeriod(
                period_month=period_month.replace(day=1),
                status="draft",
                electricity_bill_amount=electricity_bill_amount,
                electricity_rate=electricity_rate,
                electricity_rate_is_manual=electricity_rate_is_manual,
                water_rate=water_rate,
                note=note,
            )
            db.add(new_period)
            db.flush()
            db.refresh(new_period)
            return _to_billing_period_response(new_period), None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="create_billing_period_psql",
                type_error="integrity_error",
                key_type_error="IntegrityError",
            ),
            False,
        )
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="create_billing_period_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def create_meter_reading_psql(
    period_id: str,
    meter_id: str,
    previous_value: float,
    current_value: float,
    error_correction: float = 0,
    db_session: Session | None = None,
) -> tuple[MeterReadingResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            new_reading = RentalMeterReading(
                period_id=period_id,
                meter_id=meter_id,
                previous_value=previous_value,
                current_value=current_value,
                error_correction=error_correction,
            )
            db.add(new_reading)
            db.flush()
            db.refresh(new_reading)
            return _to_meter_reading_response(new_reading), None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="create_meter_reading_psql",
                type_error="integrity_error",
                key_type_error="IntegrityError",
            ),
            False,
        )
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="create_meter_reading_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def create_settlement_psql(
    period_id: str,
    apartment_id: str,
    tenancy_id: str | None,
    rent_amount: float,
    electricity_consumption: float,
    electricity_cost: float,
    water_consumption: float,
    water_cost: float,
    total_media_amount: float,
    total_amount: float,
    items: list[SettlementItemInput],
    note: str | None = None,
    db_session: Session | None = None,
) -> tuple[SettlementResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            new_settlement = RentalSettlement(
                period_id=period_id,
                apartment_id=apartment_id,
                tenancy_id=tenancy_id,
                rent_amount=rent_amount,
                electricity_consumption=electricity_consumption,
                electricity_cost=electricity_cost,
                water_consumption=water_consumption,
                water_cost=water_cost,
                total_media_amount=total_media_amount,
                total_amount=total_amount,
                note=note,
            )
            db.add(new_settlement)
            db.flush()

            new_items = []
            for item in items:
                new_item = RentalSettlementItem(
                    settlement_id=new_settlement.id,
                    cost_type_id=item.cost_type_id,
                    name=item.name,
                    kind=item.kind,
                    amount=item.amount,
                )
                db.add(new_item)
                new_items.append(new_item)
            db.flush()

            db.refresh(new_settlement)
            for new_item in new_items:
                db.refresh(new_item)
            return _to_settlement_response(new_settlement, new_items), None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="create_settlement_psql",
                type_error="integrity_error",
                key_type_error="IntegrityError",
            ),
            False,
        )
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="create_settlement_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
