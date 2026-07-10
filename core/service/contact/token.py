"""Token kontaktowy (X-Contact-Token) — wspólny sekret HS256 dla klientów
publicznego endpointu /contact/messages/create.

Klienci (frontendy JS przez `jose`, backendy przez PyJWT) podpisują krótkożyciowy
token z claimem `application`; backend weryfikuje podpis i wygaśnięcie tym samym
sekretem (SECRET_KEY_CONTACT_TOKEN). Przykłady klientów: docs/CONTACT_TOKEN.md.
"""

from datetime import datetime, timedelta, timezone

import jwt

from api.response import ApiErrorData
from config.settings import settings


def encode_contact_token(application: str, expires_minutes: int = 5) -> str:
    """Podpisuje token kontaktowy — odpowiednik tego, co robią klienci (używane w testach
    i przez backendy wołające endpoint kontaktowy z tego samego kodu)."""
    now = datetime.now(timezone.utc)
    payload = {"application": application, "exp": now + timedelta(minutes=expires_minutes), "iat": now}
    return jwt.encode(payload, settings.secret_key_contact_token, algorithm=settings.algorithm)


def decode_contact_token(token: str) -> tuple[str | None, ApiErrorData | None, bool]:
    """Weryfikuje token kontaktowy i zwraca claim `application`.

    Wymaga `exp` (token bez wygaśnięcia jest odrzucany) i niepustego `application`.
    """

    def _error(message: str, type_error: str) -> tuple[None, ApiErrorData, bool]:
        return (
            None,
            ApiErrorData(
                message=message,
                type_module="decode_contact_token",
                type_error=type_error,
                key_type_error="Unauthorized",
            ),
            False,
        )

    try:
        payload = jwt.decode(
            token,
            settings.secret_key_contact_token,
            algorithms=[settings.algorithm],
            options={"require": ["exp"]},
        )

        application = payload.get("application")
        if not application or not str(application).strip():
            return _error("Token has no 'application' claim.", "invalid_token")

        return str(application).strip(), None, True

    except jwt.ExpiredSignatureError:
        return _error("Contact token has expired.", "token_expired")
    except jwt.MissingRequiredClaimError:
        return _error("Contact token has no 'exp' claim.", "invalid_token")
    except jwt.InvalidTokenError as e:
        return _error(f"Invalid contact token: {e}", "invalid_token")
