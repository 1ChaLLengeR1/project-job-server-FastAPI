from consumer.data.response import ResponseData, create_success_response, create_error_response
from database.db import get_db
from database.tasks.models import Tasks


def create_task_psql(description: str, time: int, active: bool = True) -> ResponseData:
    db = next(get_db())
    try:
        new_task = Tasks(
            description=description,
            time=time,
            active=active
        )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        return create_success_response(data=new_task, status_code=200)
    except Exception as e:
        db.rollback()
        return create_error_response(message=str(e), status_code=417)
    finally:
        db.close()
