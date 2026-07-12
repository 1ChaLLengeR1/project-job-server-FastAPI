from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.logs.create import create_logs_psql
from core.repository.psql.rental.billing.collection import (
    collection_billing_periods_psql,
    collection_meter_readings_psql,
    collection_settlements_psql,
)
from core.repository.psql.rental.billing.response import (
    BillingPeriodResponse,
    MeterReadingResponse,
    SettlementResponse,
)


def handler_collection_billing_periods(
    user_id: str, status: str | None = None, db_session: Session | None = None
) -> tuple[list[BillingPeriodResponse] | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = collection_billing_periods_psql(status, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:collection_billing_periods", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_collection_billing_periods",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def handler_collection_meter_readings(
    user_id: str, period_id: str, db_session: Session | None = None
) -> tuple[list[MeterReadingResponse] | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = collection_meter_readings_psql(period_id, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:collection_meter_readings", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_collection_meter_readings",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def handler_collection_settlements(
    user_id: str,
    period_id: str | None = None,
    apartment_id: str | None = None,
    db_session: Session | None = None,
) -> tuple[list[SettlementResponse] | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = collection_settlements_psql(period_id, apartment_id, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:collection_settlements", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_collection_settlements",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
