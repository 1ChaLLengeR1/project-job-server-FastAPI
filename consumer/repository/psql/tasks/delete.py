from consumer.data.response import ResponseData, create_success_response, create_error_response
from database.db import get_db
from database.tasks.models import Tasks


def delete_task_psql(task_id: str) -> ResponseData:
    db = next(get_db())
    try:
        task = db.query(Tasks).filter(Tasks.id == task_id).first()
        if not task:
            return create_error_response(message="Task nie istnieje", status_code=404)

        deleted_task = task
        db.delete(task)
        db.commit()

        return create_success_response(data=deleted_task, status_code=200)
    except Exception as e:
        db.rollback()
        return create_error_response(message=str(e), status_code=417)
    finally:
        db.close()
