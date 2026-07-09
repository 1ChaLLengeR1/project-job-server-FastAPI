from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.logs.create import create_logs_psql
from core.repository.psql.tasks.create import create_task_psql
from core.repository.psql.tasks.response import TaskResponse


def handler_create_task(
    user_id: str,
    description: str,
    time: int,
    active: bool = True,
    db_session: Session | None = None,
) -> tuple[TaskResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = create_task_psql(description, time, active, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "tasks:create", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_create_task",
            type_error="exception",
            key_type_error="Exception",
        ), False
