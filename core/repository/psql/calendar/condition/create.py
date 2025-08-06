from core.data.response import ResponseData, create_success_response, create_error_response
from database.db import get_db
from sqlalchemy.orm import Session
from database.calendar.models import WorkConditionChange
from sqlalchemy.exc import IntegrityError
from datetime import datetime


def create_work_condition_change_psql(norm_hours: float, hourly_rate: float) -> ResponseData:
    db_generator = get_db()
    db: Session = next(db_generator)
    try:
        new_condition = WorkConditionChange(
            start_date=datetime.now(),
            norm_hours=norm_hours,
            hourly_rate=hourly_rate
        )

        db.add(new_condition)
        db.commit()
        db.refresh(new_condition)

        response_data = {
            "id": str(new_condition.id),
            "start_date": new_condition.start_date.isoformat(),
            "norm_hours": new_condition.norm_hours,
            "hourly_rate": new_condition.hourly_rate,
            "created_at": new_condition.created_at.isoformat(),
            "updated_at": new_condition.updated_at.isoformat()
        }

        return create_success_response(
            data=response_data,
            status_code=201
        )

    except IntegrityError as e:
        db.rollback()
        return create_error_response(
            message=f"create_work_condition_change_psql IntegrityError: {e}",
            status_code=409
        )
    except Exception as e:
        db.rollback()
        return create_error_response(
            message=f"create_work_condition_change_psql Exception: {str(e)}",
            status_code=417
        )
    finally:
        db.close()
