from datetime import date

from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.logs.response import LogResponse, _to_log_response
from database.psql.database import managed_session
from database.psql.models.auth import Users
from database.psql.models.logs import Logs


def create_logs_psql(
    user_id: str, description: str, db_session: Session | None = None
) -> tuple[LogResponse | None, ApiErrorData | None, bool]:
    """Audytowy zapis akcji usera — wołany z handlerów po udanej operacji.

    `description` opisuje moduł/akcję slugiem `{domain}:{action}`, np. "tasks:create".
    Username dociągany z tabeli users po `user_id` (z tokenu, nie od klienta).
    """
    try:
        with managed_session(db_session) as (db, _):
            user = db.query(Users).filter(Users.id == user_id).first()
            if not user:
                return None, ApiErrorData(
                    message=f"Not found user with id: {user_id}",
                    type_module="create_logs_psql",
                    type_error="not_found",
                    key_type_error="NotFound",
                ), False

            new_log = Logs(username=user.username, description=description, date=date.today())
            db.add(new_log)
            db.flush()
            db.refresh(new_log)
            return _to_log_response(new_log), None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="create_logs_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
