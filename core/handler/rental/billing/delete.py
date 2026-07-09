from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.logs.create import create_logs_psql
from core.repository.psql.rental.billing.delete import (
    delete_billing_period_psql,
    delete_meter_reading_psql,
)
from core.repository.psql.rental.billing.response import BillingPeriodResponse, MeterReadingResponse


def handler_delete_billing_period(
    user_id: str, period_id: str, db_session: Session | None = None
) -> tuple[BillingPeriodResponse | None, ApiErrorData | None, bool]:
    """Pełne wycofanie okresu — kasuje odczyty i snapshoty rozliczeń."""
    try:
        result, err, ok = delete_billing_period_psql(period_id, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:delete_billing_period", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_delete_billing_period",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def handler_delete_meter_reading(
    user_id: str, reading_id: str, db_session: Session | None = None
) -> tuple[MeterReadingResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = delete_meter_reading_psql(reading_id, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:delete_meter_reading", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_delete_meter_reading",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
