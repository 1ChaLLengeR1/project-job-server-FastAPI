from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.calendar.response import CalendarStatisticsResponse
from core.repository.psql.calendar.statistics import statistics_calendar_psql
from core.repository.psql.logs.create import create_logs_psql


def handler_statistics_calendar(
    user_id: str, year: int, db_session: Session | None = None
) -> tuple[CalendarStatisticsResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = statistics_calendar_psql(year, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "calendar:statistics", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_statistics_calendar",
            type_error="exception",
            key_type_error="Exception",
        ), False
