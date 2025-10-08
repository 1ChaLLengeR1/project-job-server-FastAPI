from core.data.response import ResponseData, create_success_response, create_error_response
from database.db import get_db
from database.tasks.models import Tasks
from api.tasks.schemas import ResponseSerializerTask


def delete_task_psql(task_id: str) -> ResponseData:
    db = next(get_db())
    try:
        task = db.query(Tasks).filter(Tasks.id == task_id).first()
        if not task:
            return create_error_response(message="Task nie istnieje", status_code=404)

        deleted_task = task
        db.delete(task)
        db.commit()

        task_data = ResponseSerializerTask.from_orm(deleted_task)
        return create_success_response(data=task_data.model_dump(mode="json"), status_code=200)
    except Exception as e:
        db.rollback()
        return create_error_response(message=str(e), status_code=417)
    finally:
        db.close()
