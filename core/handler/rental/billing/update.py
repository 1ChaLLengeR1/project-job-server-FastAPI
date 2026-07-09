from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.logs.create import create_logs_psql
from core.repository.psql.rental.billing.one import one_billing_period_psql
from core.repository.psql.rental.billing.response import BillingPeriodResponse, MeterReadingResponse
from core.repository.psql.rental.billing.update import (
    update_billing_period_psql,
    update_meter_reading_psql,
)


def handler_update_billing_period(
    user_id: str,
    period_id: str,
    new_electricity_bill_amount: float | None,
    new_electricity_rate: float | None,
    new_electricity_rate_is_manual: bool,
    new_water_rate: float,
    new_note: str | None,
    db_session: Session | None = None,
) -> tuple[BillingPeriodResponse | None, ApiErrorData | None, bool]:
    try:
        period, err, ok = one_billing_period_psql(period_id, db_session=db_session)
        if not ok:
            return None, err, False
        if period.status == "closed":
            return (
                None,
                ApiErrorData(
                    message="Okres jest zamknięty — najpierw otwórz go ponownie (reopen)",
                    type_module="handler_update_billing_period",
                    type_error="integrity_error",
                    key_type_error="IntegrityError",
                ),
                False,
            )

        result, err, ok = update_billing_period_psql(
            period_id,
            new_electricity_bill_amount,
            new_electricity_rate,
            new_electricity_rate_is_manual,
            new_water_rate,
            new_note,
            db_session=db_session,
        )
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:update_billing_period", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_update_billing_period",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def handler_update_meter_reading(
    user_id: str,
    reading_id: str,
    new_previous_value: float,
    new_current_value: float,
    new_error_correction: float,
    db_session: Session | None = None,
) -> tuple[MeterReadingResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = update_meter_reading_psql(
            reading_id, new_previous_value, new_current_value, new_error_correction, db_session=db_session
        )
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:update_meter_reading", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_update_meter_reading",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
