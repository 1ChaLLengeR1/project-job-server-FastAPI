from consumer.data.response import ResponseData, create_success_response, create_error_response
from database.db import get_db
from database.tasks.models import Tasks


def collection_tasks_psql(active: bool = True) -> ResponseData:
    db = next(get_db())
    try:
        tasks = (
            db.query(Tasks)
            .filter(Tasks.active == active)
            .order_by(Tasks.time.asc())
            .all()
        )
        return create_success_response(data=tasks, status_code=200)
    except Exception as e:
        db.rollback()
        return create_error_response(message=str(e), status_code=417)
    finally:
        db.close()
