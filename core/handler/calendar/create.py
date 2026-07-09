from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.calendar.create import create_generator_calendar_psql
from core.repository.psql.calendar.response import GeneratedCalendarResponse
from core.repository.psql.logs.create import create_logs_psql
from core.service.calendar.holidays import fetch_public_holidays


def handler_create_generator_calendar(
    user_id: str, year: int, db_session: Session | None = None
) -> tuple[GeneratedCalendarResponse | None, ApiErrorData | None, bool]:
    try:
        holidays, err, ok = fetch_public_holidays(year, "PL")
        if not ok:
            return None, err, False

        holiday_days = {holiday.date_object for holiday in holidays}

        result, err, ok = create_generator_calendar_psql(year, holiday_days, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "calendar:create", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_create_generator_calendar",
            type_error="exception",
            key_type_error="Exception",
        ), False
