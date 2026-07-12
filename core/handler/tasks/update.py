from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.logs.create import create_logs_psql
from core.repository.psql.tasks.response import TaskResponse
from core.repository.psql.tasks.update import update_task_active_psql, update_task_psql


def handler_update_task(
    user_id: str,
    task_id: str,
    new_description: str,
    new_time: int,
    db_session: Session | None = None,
) -> tuple[TaskResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = update_task_psql(task_id, new_description, new_time, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "tasks:update", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_update_task",
            type_error="exception",
            key_type_error="Exception",
        ), False


def handler_update_task_active(
    user_id: str, task_id: str, new_active: bool, db_session: Session | None = None
) -> tuple[TaskResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = update_task_active_psql(task_id, new_active, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "tasks:update_active", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_update_task_active",
            type_error="exception",
            key_type_error="Exception",
        ), False
