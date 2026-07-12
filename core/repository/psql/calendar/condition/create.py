from datetime import date

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.calendar.condition.response import WorkConditionResponse, _to_work_condition_response
from database.psql.database import managed_session
from database.psql.models.calendar import WorkConditionChange


def create_work_condition_change_psql(
    norm_hours: float, hourly_rate: float, db_session: Session | None = None
) -> tuple[WorkConditionResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            new_condition = WorkConditionChange(
                start_date=date.today(), norm_hours=norm_hours, hourly_rate=hourly_rate
            )
            db.add(new_condition)
            db.flush()
            db.refresh(new_condition)
            return _to_work_condition_response(new_condition), None, True
    except IntegrityError as e:
        return None, ApiErrorData(
            message=str(e.orig),
            type_module="create_work_condition_change_psql",
            type_error="integrity_error",
            key_type_error="IntegrityError",
        ), False
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="create_work_condition_change_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
