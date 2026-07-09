from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.tasks.response import TaskResponse, _to_task_response
from database.psql.database import managed_session
from database.psql.models.tasks import Tasks


def update_task_psql(
    task_id: str, new_description: str, new_time: int, db_session: Session | None = None
) -> tuple[TaskResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            task = db.query(Tasks).filter(Tasks.id == task_id).first()
            if not task:
                return None, ApiErrorData(
                    message="Task nie istnieje",
                    type_module="update_task_psql",
                    type_error="not_found",
                    key_type_error="NotFound",
                ), False

            task.description = new_description
            task.time = new_time
            db.flush()
            db.refresh(task)
            return _to_task_response(task), None, True
    except IntegrityError as e:
        return None, ApiErrorData(
            message=str(e.orig),
            type_module="update_task_psql",
            type_error="integrity_error",
            key_type_error="IntegrityError",
        ), False
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="update_task_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False


def update_task_active_psql(
    task_id: str, new_active: bool, db_session: Session | None = None
) -> tuple[TaskResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            task = db.query(Tasks).filter(Tasks.id == task_id).first()
            if not task:
                return None, ApiErrorData(
                    message="Task nie istnieje",
                    type_module="update_task_active_psql",
                    type_error="not_found",
                    key_type_error="NotFound",
                ), False

            task.active = new_active
            db.flush()
            db.refresh(task)
            return _to_task_response(task), None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="update_task_active_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
