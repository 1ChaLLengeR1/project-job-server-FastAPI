from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.rental.billing.response import (
    BillingPeriodResponse,
    MeterReadingResponse,
    _to_billing_period_response,
    _to_meter_reading_response,
)
from database.psql.database import managed_session
from database.psql.models.rentals import RentalBillingPeriod, RentalMeterReading


def update_billing_period_psql(
    period_id: str,
    new_electricity_bill_amount: float | None,
    new_electricity_rate: float | None,
    new_electricity_rate_is_manual: bool,
    new_water_rate: float,
    new_note: str | None,
    db_session: Session | None = None,
) -> tuple[BillingPeriodResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            period = db.query(RentalBillingPeriod).filter(RentalBillingPeriod.id == period_id).first()
            if not period:
                return (
                    None,
                    ApiErrorData(
                        message="Okres rozliczeniowy nie istnieje",
                        type_module="update_billing_period_psql",
                        type_error="not_found",
                        key_type_error="NotFound",
                    ),
                    False,
                )

            period.electricity_bill_amount = new_electricity_bill_amount
            period.electricity_rate = new_electricity_rate
            period.electricity_rate_is_manual = new_electricity_rate_is_manual
            period.water_rate = new_water_rate
            period.note = new_note
            db.flush()
            db.refresh(period)
            return _to_billing_period_response(period), None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="update_billing_period_psql",
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
                type_module="update_billing_period_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def update_billing_period_status_psql(
    period_id: str, new_status: str, db_session: Session | None = None
) -> tuple[BillingPeriodResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            period = db.query(RentalBillingPeriod).filter(RentalBillingPeriod.id == period_id).first()
            if not period:
                return (
                    None,
                    ApiErrorData(
                        message="Okres rozliczeniowy nie istnieje",
                        type_module="update_billing_period_status_psql",
                        type_error="not_found",
                        key_type_error="NotFound",
                    ),
                    False,
                )

            period.status = new_status
            db.flush()
            db.refresh(period)
            return _to_billing_period_response(period), None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="update_billing_period_status_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def update_meter_reading_psql(
    reading_id: str,
    new_previous_value: float,
    new_current_value: float,
    new_error_correction: float,
    db_session: Session | None = None,
) -> tuple[MeterReadingResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            reading = db.query(RentalMeterReading).filter(RentalMeterReading.id == reading_id).first()
            if not reading:
                return (
                    None,
                    ApiErrorData(
                        message="Odczyt licznika nie istnieje",
                        type_module="update_meter_reading_psql",
                        type_error="not_found",
                        key_type_error="NotFound",
                    ),
                    False,
                )

            reading.previous_value = new_previous_value
            reading.current_value = new_current_value
            reading.error_correction = new_error_correction
            db.flush()
            db.refresh(reading)
            return _to_meter_reading_response(reading), None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="update_meter_reading_psql",
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
                type_module="update_meter_reading_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
