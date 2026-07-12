from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.tasks.response import TaskResponse, _to_task_response
from database.psql.database import managed_session
from database.psql.models.tasks import Tasks


def create_task_psql(
    description: str, time: int, active: bool = True, db_session: Session | None = None
) -> tuple[TaskResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            new_task = Tasks(description=description, time=time, active=active)
            db.add(new_task)
            db.flush()
            db.refresh(new_task)
            return _to_task_response(new_task), None, True
    except IntegrityError as e:
        return None, ApiErrorData(
            message=str(e.orig),
            type_module="create_task_psql",
            type_error="integrity_error",
            key_type_error="IntegrityError",
        ), False
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="create_task_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
