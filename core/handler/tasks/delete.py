from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.logs.create import create_logs_psql
from core.repository.psql.tasks.delete import delete_task_psql
from core.repository.psql.tasks.response import TaskResponse


def handler_delete_task(
    user_id: str, task_id: str, db_session: Session | None = None
) -> tuple[TaskResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = delete_task_psql(task_id, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "tasks:delete", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_delete_task",
            type_error="exception",
            key_type_error="Exception",
        ), False
