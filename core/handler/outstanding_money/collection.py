from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.logs.create import create_logs_psql
from core.repository.psql.outstanding_money.collection import collection_list_psql
from core.repository.psql.outstanding_money.response import OverdueListResponse


def handler_collection_list(
    user_id: str, db_session: Session | None = None
) -> tuple[list[OverdueListResponse] | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = collection_list_psql(db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "outstanding_money:collection", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_collection_list",
            type_error="exception",
            key_type_error="Exception",
        ), False
