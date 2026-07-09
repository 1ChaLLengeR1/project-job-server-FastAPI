from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.calendar.collection import collection_calendar_psql
from core.repository.psql.calendar.response import CalendarCollectionResponse
from core.repository.psql.logs.create import create_logs_psql


def handler_collection_calendar(
    user_id: str, year: int, month: int, db_session: Session | None = None
) -> tuple[CalendarCollectionResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = collection_calendar_psql(year, month, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "calendar:collection", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_collection_calendar",
            type_error="exception",
            key_type_error="Exception",
        ), False
