from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.tasks.response import TaskResponse, _to_task_response
from database.psql.database import managed_session
from database.psql.models.tasks import Tasks


def delete_task_psql(
    task_id: str, db_session: Session | None = None
) -> tuple[TaskResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            task = db.query(Tasks).filter(Tasks.id == task_id).first()
            if not task:
                return None, ApiErrorData(
                    message="Task nie istnieje",
                    type_module="delete_task_psql",
                    type_error="not_found",
                    key_type_error="NotFound",
                ), False

            deleted_task = _to_task_response(task)
            db.delete(task)
            db.flush()
            return deleted_task, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="delete_task_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
