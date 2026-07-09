from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.calendar.condition.response import WorkConditionResponse, _to_work_condition_response
from database.psql.database import managed_session
from database.psql.models.calendar import WorkConditionChange


def collection_work_condition_changes_psql(
    db_session: Session | None = None,
) -> tuple[list[WorkConditionResponse] | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            work_conditions = db.query(WorkConditionChange).order_by(WorkConditionChange.start_date.desc()).all()
            return [_to_work_condition_response(condition) for condition in work_conditions], None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="collection_work_condition_changes_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
