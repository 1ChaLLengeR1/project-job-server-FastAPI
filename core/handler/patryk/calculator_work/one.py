from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.logs.create import create_logs_psql
from core.repository.psql.patryk.one import one_calculator_keys_psql
from core.repository.psql.patryk.response import KeysCalculatorResponse


def handler_one_calculator_keys(
    user_id: str, db_session: Session | None = None
) -> tuple[KeysCalculatorResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = one_calculator_keys_psql(db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "calculator_work:one", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_one_calculator_keys",
            type_error="exception",
            key_type_error="Exception",
        ), False
