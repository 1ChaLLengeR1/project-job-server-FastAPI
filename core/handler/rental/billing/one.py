from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.logs.create import create_logs_psql
from core.repository.psql.rental.billing.one import one_billing_period_psql, one_settlement_psql
from core.repository.psql.rental.billing.response import BillingPeriodResponse, SettlementResponse


def handler_one_billing_period(
    user_id: str, period_id: str, db_session: Session | None = None
) -> tuple[BillingPeriodResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = one_billing_period_psql(period_id, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:one_billing_period", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_one_billing_period",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def handler_one_settlement(
    user_id: str, settlement_id: str, db_session: Session | None = None
) -> tuple[SettlementResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = one_settlement_psql(settlement_id, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:one_settlement", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_one_settlement",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
