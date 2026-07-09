import uuid
from datetime import datetime, timedelta, timezone

import jwt

from api.response import ApiErrorData
from config.settings import settings


def encode_access_token(user_id: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {"id": user_id, "exp": now + timedelta(hours=settings.token_expires_hours), "iat": now}
    return jwt.encode(payload, settings.secret_key_token, algorithm=settings.algorithm)


def encode_refresh_token(user_id: str) -> str:
    now = datetime.now(timezone.utc)
    # UWAGA: zachowanie historyczne — REFRESH_TOKEN_EXPIRES_HOURS jest interpretowane jako DNI
    payload = {"id": user_id, "exp": now + timedelta(days=settings.refresh_token_expires_hours), "iat": now}
    return jwt.encode(payload, settings.secret_key_refresh_token, algorithm=settings.algorithm)


def _decode_token(token: str, secret: str, type_module: str) -> tuple[str | None, ApiErrorData | None, bool]:
    def _error(message: str, type_error: str) -> tuple[None, ApiErrorData, bool]:
        return None, ApiErrorData(
            message=message,
            type_module=type_module,
            type_error=type_error,
            key_type_error="Unauthorized",
        ), False

    try:
        payload = jwt.decode(token, secret, algorithms=[settings.algorithm])

        user_id = payload.get("id")
        if not user_id:
            return _error("Token has no 'id' claim.", "invalid_token")

        try:
            uuid.UUID(str(user_id))
        except ValueError:
            return _error("Claim 'id' is not a valid UUID.", "invalid_token")

        return str(user_id), None, True

    except jwt.ExpiredSignatureError:
        return _error("Token has expired.", "token_expired")
    except jwt.InvalidTokenError as e:
        return _error(f"Invalid token: {e}", "invalid_token")


def decode_access_token(token: str) -> tuple[str | None, ApiErrorData | None, bool]:
    """Weryfikuje access token i zwraca user_id z claimu."""
    return _decode_token(token, settings.secret_key_token, "decode_access_token")


def decode_refresh_token(token: str, expected_user_id: str) -> tuple[str | None, ApiErrorData | None, bool]:
    """Weryfikuje refresh token i sprawdza, czy claim `id` zgadza się z żądanym userem."""
    user_id, err, ok = _decode_token(token, settings.secret_key_refresh_token, "decode_refresh_token")
    if not ok:
        return None, err, False

    if user_id != expected_user_id:
        return None, ApiErrorData(
            message="Refresh token does not belong to this user.",
            type_module="decode_refresh_token",
            type_error="token_mismatch",
            key_type_error="Unauthorized",
        ), False

    return user_id, None, True
