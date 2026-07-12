from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.logs.create import create_logs_psql
from core.repository.psql.patryk.one import one_calculator_keys_psql
from core.service.patryk.calculation import calculation_profit
from core.service.patryk.response import CalculationResponse


def handler_calculations(
    user_id: str,
    gross_sales: float,
    gross_purchase: float,
    provision: float,
    distinction: float,
    referrer: str,
    db_session: Session | None = None,
) -> tuple[CalculationResponse | None, ApiErrorData | None, bool]:
    try:
        keys, err, ok = one_calculator_keys_psql(db_session=db_session)
        if not ok:
            return None, err, False

        result, err, ok = calculation_profit(keys, gross_sales, gross_purchase, provision, distinction, referrer)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "calculator_work:calculations", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_calculations",
            type_error="exception",
            key_type_error="Exception",
        ), False
