from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.calendar.condition.collection import collection_work_condition_changes_psql
from core.repository.psql.calendar.condition.response import WorkConditionResponse
from core.repository.psql.logs.create import create_logs_psql


def handler_collection_work_condition_changes(
    user_id: str, db_session: Session | None = None
) -> tuple[list[WorkConditionResponse] | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = collection_work_condition_changes_psql(db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "calendar_condition:collection", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_collection_work_condition_changes",
            type_error="exception",
            key_type_error="Exception",
        ), False
