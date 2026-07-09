from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.logs.response import LogResponse, _to_log_response
from database.psql.database import managed_session
from database.psql.models.logs import Logs


def collection_logs_psql(
    number: int, db_session: Session | None = None
) -> tuple[list[LogResponse] | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            query = db.query(Logs).order_by(Logs.date.desc())
            if number > 0:
                query = query.limit(number)
            row_logs = query.all()

            return [_to_log_response(log) for log in row_logs], None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="collection_logs_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
