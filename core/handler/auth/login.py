from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.helper.password import verify_password
from core.repository.psql.logs.create import create_logs_psql
from core.repository.psql.user.one import one_user_credentials_by_username_psql
from core.service.auth.response import AuthTokensResponse
from core.service.auth.tokens import encode_access_token, encode_refresh_token


def _invalid_credentials(type_module: str) -> tuple[None, ApiErrorData, bool]:
    # Generyczny komunikat — nie zdradzamy, czy istnieje user o podanej nazwie
    return None, ApiErrorData(
        message="Password or user name is not correct",
        type_module=type_module,
        type_error="invalid_credentials",
        key_type_error="Unauthorized",
    ), False


def handler_login(
    username: str, password: str, db_session: Session | None = None
) -> tuple[AuthTokensResponse | None, ApiErrorData | None, bool]:
    try:
        user, err, ok = one_user_credentials_by_username_psql(username, db_session=db_session)
        if not ok:
            if err.key_type_error == "NotFound":
                return _invalid_credentials("handler_login")
            return None, err, False

        if not verify_password(password, user.password):
            return _invalid_credentials("handler_login")

        tokens = AuthTokensResponse(
            id=user.id,
            username=user.username,
            access_token=encode_access_token(user.id),
            refresh_token=encode_refresh_token(user.id),
        )

        create_logs_psql(user.id, "auth:login", db_session=db_session)
        return tokens, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_login",
            type_error="exception",
            key_type_error="Exception",
        ), False


def handler_automatically_login(
    user_id: str, username: str, db_session: Session | None = None
) -> tuple[AuthTokensResponse | None, ApiErrorData | None, bool]:
    """Autoryzację refresh tokenu robi JWTRefreshAuthenticationMiddleware —
    handler tylko wystawia nowe tokeny i zapisuje audyt."""
    try:
        tokens = AuthTokensResponse(
            id=user_id,
            username=username,
            access_token=encode_access_token(user_id),
            refresh_token=encode_refresh_token(user_id),
        )

        create_logs_psql(user_id, "auth:automatically_login", db_session=db_session)
        return tokens, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_automatically_login",
            type_error="exception",
            key_type_error="Exception",
        ), False
