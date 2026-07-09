from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.calendar.condition.create import create_work_condition_change_psql
from core.repository.psql.calendar.condition.response import WorkConditionResponse
from core.repository.psql.logs.create import create_logs_psql


def handler_create_work_condition_change(
    user_id: str, norm_hours: float, hourly_rate: float, db_session: Session | None = None
) -> tuple[WorkConditionResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = create_work_condition_change_psql(norm_hours, hourly_rate, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "calendar_condition:create", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_create_work_condition_change",
            type_error="exception",
            key_type_error="Exception",
        ), False
