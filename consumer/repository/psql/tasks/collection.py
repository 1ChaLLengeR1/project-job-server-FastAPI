from api.tasks.schemas import ResponseSerializerTask
from consumer.data.response import ResponseData, create_success_response, create_error_response
from database.db import get_db
from database.tasks.models import Tasks


def collection_tasks_psql(active: bool = True) -> ResponseData:
    db = next(get_db())
    try:
        tasks = (
            db.query(Tasks)
            .filter(Tasks.active == active)
            .order_by(Tasks.updated_at.desc())
            .all()
        )

        task_data = [ResponseSerializerTask.from_orm(task) for task in tasks]
        serialized = [task.model_dump(mode="json") for task in task_data]
        return create_success_response(data=serialized, status_code=200)
    except Exception as e:
        db.rollback()
        return create_error_response(message=str(e), status_code=417)
    finally:
        db.close()
