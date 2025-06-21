from api.tasks.schemas import ResponseSerializerTask
from consumer.data.response import ResponseData, create_success_response, create_error_response
from database.db import get_db
from database.tasks.models import Tasks


def update_task_psql(task_id: str, new_description: str, new_time: int) -> ResponseData:
    db = next(get_db())
    try:
        task = db.query(Tasks).filter(Tasks.id == task_id).first()
        if not task:
            return create_error_response(message="Task nie istnieje", status_code=400)

        task.description = new_description
        task.time = new_time
        db.commit()
        db.refresh(task)

        task_data = ResponseSerializerTask.from_orm(task)
        return create_success_response(data=task_data.model_dump(mode="json"), status_code=200)
    except Exception as e:
        db.rollback()
        return create_error_response(message=str(e), status_code=417)
    finally:
        db.close()


def update_task_active_psql(task_id: str, new_active: bool) -> ResponseData:
    db = next(get_db())
    try:
        task = db.query(Tasks).filter(Tasks.id == task_id).first()
        if not task:
            return create_error_response(message="Task nie istnieje", status_code=400)

        task.active = new_active
        db.commit()
        db.refresh(task)

        task_data = ResponseSerializerTask.from_orm(task)
        return create_success_response(data=task_data.model_dump(mode="json"), status_code=200)
    except Exception as e:
        db.rollback()
        return create_error_response(message=str(e), status_code=417)
    finally:
        db.close()
