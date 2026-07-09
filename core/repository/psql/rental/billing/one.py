from datetime import date

from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.rental.billing.response import (
    BillingPeriodResponse,
    MeterReadingResponse,
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


def one_billing_period_psql(
    period_id: str, db_session: Session | None = None
) -> tuple[BillingPeriodResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            period = db.query(RentalBillingPeriod).filter(RentalBillingPeriod.id == period_id).first()
            if not period:
                return (
                    None,
                    ApiErrorData(
                        message="Okres rozliczeniowy nie istnieje",
                        type_module="one_billing_period_psql",
                        type_error="not_found",
                        key_type_error="NotFound",
                    ),
                    False,
                )
            return _to_billing_period_response(period), None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="one_billing_period_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def one_billing_period_by_month_psql(
    period_month: date, db_session: Session | None = None
) -> tuple[BillingPeriodResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            period = (
                db.query(RentalBillingPeriod)
                .filter(RentalBillingPeriod.period_month == period_month.replace(day=1))
                .first()
            )
            if not period:
                return (
                    None,
                    ApiErrorData(
                        message="Okres rozliczeniowy nie istnieje",
                        type_module="one_billing_period_by_month_psql",
                        type_error="not_found",
                        key_type_error="NotFound",
                    ),
                    False,
                )
            return _to_billing_period_response(period), None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="one_billing_period_by_month_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def one_meter_reading_psql(
    reading_id: str, db_session: Session | None = None
) -> tuple[MeterReadingResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            reading = db.query(RentalMeterReading).filter(RentalMeterReading.id == reading_id).first()
            if not reading:
                return (
                    None,
                    ApiErrorData(
                        message="Odczyt licznika nie istnieje",
                        type_module="one_meter_reading_psql",
                        type_error="not_found",
                        key_type_error="NotFound",
                    ),
                    False,
                )
            return _to_meter_reading_response(reading), None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="one_meter_reading_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def one_last_meter_reading_psql(
    meter_id: str, db_session: Session | None = None
) -> tuple[MeterReadingResponse | None, ApiErrorData | None, bool]:
    """Ostatni odczyt licznika (wg miesiąca okresu) — do prefillu previous_value nowego okresu."""
    try:
        with managed_session(db_session) as (db, _):
            reading = (
                db.query(RentalMeterReading)
                .join(RentalBillingPeriod, RentalMeterReading.period_id == RentalBillingPeriod.id)
                .filter(RentalMeterReading.meter_id == meter_id)
                .order_by(RentalBillingPeriod.period_month.desc())
                .first()
            )
            if not reading:
                return (
                    None,
                    ApiErrorData(
                        message="Brak odczytów dla tego licznika",
                        type_module="one_last_meter_reading_psql",
                        type_error="not_found",
                        key_type_error="NotFound",
                    ),
                    False,
                )
            return _to_meter_reading_response(reading), None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="one_last_meter_reading_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def one_settlement_psql(
    settlement_id: str, db_session: Session | None = None
) -> tuple[SettlementResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            settlement = db.query(RentalSettlement).filter(RentalSettlement.id == settlement_id).first()
            if not settlement:
                return (
                    None,
                    ApiErrorData(
                        message="Rozliczenie nie istnieje",
                        type_module="one_settlement_psql",
                        type_error="not_found",
                        key_type_error="NotFound",
                    ),
                    False,
                )

            items = (
                db.query(RentalSettlementItem)
                .filter(RentalSettlementItem.settlement_id == settlement.id)
                .order_by(RentalSettlementItem.created_at.asc())
                .all()
            )
            return _to_settlement_response(settlement, items), None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="one_settlement_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
