from core.data.response import ResponseData, create_success_response, create_error_response
from database.db import get_db
from sqlalchemy.orm import Session
from database.calendar.models import WorkConditionChange


def collection_work_condition_changes_psql() -> ResponseData:
    db_generator = get_db()
    db: Session = next(db_generator)
    try:
        work_conditions = db.query(WorkConditionChange).order_by(
            WorkConditionChange.start_date.desc()
        ).all()

        response_data = []
        for condition in work_conditions:
            condition_data = {
                "id": str(condition.id),
                "start_date": condition.start_date.isoformat(),
                "norm_hours": condition.norm_hours,
                "hourly_rate": condition.hourly_rate,
                "created_at": condition.created_at.isoformat(),
                "updated_at": condition.updated_at.isoformat()
            }
            response_data.append(condition_data)

        return create_success_response(
            data=response_data,
            status_code=200
        )

    except Exception as e:
        return create_error_response(
            message=f"get_all_work_condition_changes_psql Exception: {str(e)}",
            status_code=417
        )
    finally:
        db.close()
