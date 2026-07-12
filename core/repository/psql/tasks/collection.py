from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.tasks.response import TaskResponse, _to_task_response
from database.psql.database import managed_session
from database.psql.models.tasks import Tasks


def collection_tasks_psql(
    active: bool = True, db_session: Session | None = None
) -> tuple[list[TaskResponse] | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            tasks = db.query(Tasks).filter(Tasks.active == active).order_by(Tasks.updated_at.desc()).all()
            return [_to_task_response(task) for task in tasks], None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="collection_tasks_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
