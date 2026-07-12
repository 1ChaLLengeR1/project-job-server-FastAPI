from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.logs.collection import collection_logs_psql
from core.repository.psql.logs.response import LogResponse


def handler_collection_logs(
    number: int, db_session: Session | None = None
) -> tuple[list[LogResponse] | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = collection_logs_psql(number, db_session=db_session)
        if not ok:
            return None, err, False
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_collection_logs",
            type_error="exception",
            key_type_error="Exception",
        ), False
