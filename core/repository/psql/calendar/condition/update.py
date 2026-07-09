from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.calendar.condition.response import WorkConditionResponse, _to_work_condition_response
from database.psql.database import managed_session
from database.psql.models.calendar import WorkConditionChange


def update_work_condition_change_psql(
    condition_id: str, norm_hours: float, hourly_rate: float, db_session: Session | None = None
) -> tuple[WorkConditionResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            existing_condition = db.query(WorkConditionChange).filter(WorkConditionChange.id == condition_id).first()
            if not existing_condition:
                return None, ApiErrorData(
                    message=f"WorkConditionChange with id {condition_id} not found",
                    type_module="update_work_condition_change_psql",
                    type_error="not_found",
                    key_type_error="NotFound",
                ), False

            existing_condition.norm_hours = norm_hours
            existing_condition.hourly_rate = hourly_rate

            db.flush()
            db.refresh(existing_condition)
            return _to_work_condition_response(existing_condition), None, True
    except IntegrityError as e:
        return None, ApiErrorData(
            message=str(e.orig),
            type_module="update_work_condition_change_psql",
            type_error="integrity_error",
            key_type_error="IntegrityError",
        ), False
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="update_work_condition_change_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
