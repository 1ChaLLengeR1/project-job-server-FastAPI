from core.data.response import ResponseData, create_success_response, create_error_response
from database.db import get_db
from sqlalchemy.orm import Session
from database.calendar.models import WorkConditionChange
from sqlalchemy.exc import IntegrityError
import uuid


def delete_work_condition_change_psql(condition_id: str) -> ResponseData:
    db_generator = get_db()
    db: Session = next(db_generator)
    try:
        condition_uuid = uuid.UUID(condition_id)

        existing_condition = db.query(WorkConditionChange).filter(
            WorkConditionChange.id == condition_uuid
        ).first()

        if not existing_condition:
            return create_error_response(
                message=f"WorkConditionChange with id {condition_id} not found",
                status_code=404
            )

        response_data = {
            "id": str(existing_condition.id),
            "start_date": existing_condition.start_date.isoformat(),
            "norm_hours": existing_condition.norm_hours,
            "hourly_rate": existing_condition.hourly_rate,
            "created_at": existing_condition.created_at.isoformat(),
            "updated_at": existing_condition.updated_at.isoformat()
        }

        db.delete(existing_condition)
        db.commit()

        return create_success_response(
            data={
                "message": f"WorkConditionChange with id {condition_id} successfully deleted",
                "deleted_record": response_data
            },
            status_code=200
        )

    except ValueError as e:
        return create_error_response(
            message=f"delete_work_condition_change_psql - Invalid UUID format: {condition_id}",
            status_code=400
        )
    except IntegrityError as e:
        db.rollback()
        return create_error_response(
            message=f"delete_work_condition_change_psql - IntegrityError: {e}",
            status_code=409
        )
    except Exception as e:
        db.rollback()
        return create_error_response(
            message=f"delete_work_condition_change_psql - Exception: {str(e)}",
            status_code=417
        )
    finally:
        db.close()