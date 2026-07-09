from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.user.response import UserResponse, _to_user_response
from database.psql.database import managed_session
from database.psql.models.auth import Users


def one_user_by_id_psql(
    user_id: str, db_session: Session | None = None
) -> tuple[UserResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            user = db.query(Users).filter(Users.id == user_id).first()
            if not user:
                return None, ApiErrorData(
                    message=f"Not found user with id: {user_id}",
                    type_module="one_user_by_id_psql",
                    type_error="not_found",
                    key_type_error="NotFound",
                ), False
            return _to_user_response(user), None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="one_user_by_id_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
