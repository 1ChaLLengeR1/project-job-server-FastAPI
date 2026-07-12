from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.logs.create import create_logs_psql
from core.repository.psql.tasks.collection import collection_tasks_psql
from core.repository.psql.tasks.response import TaskResponse


def handler_collection_task(
    user_id: str, active: bool = True, db_session: Session | None = None
) -> tuple[list[TaskResponse] | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = collection_tasks_psql(active, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "tasks:collection", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_collection_task",
            type_error="exception",
            key_type_error="Exception",
        ), False
