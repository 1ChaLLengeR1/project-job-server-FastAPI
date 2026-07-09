import jwt
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.requests import Request

from api.response import ApiErrorData, ApiErrorResponse

# Limity per endpoint (wzorzec: docs/ARCHITEKTURA.md 7.4)
RATE_LIMIT_AUTH = "10/minute"  # login / refresh - ochrona przed brute force (klucz: IP)
RATE_LIMIT_READ = "120/minute"  # odczyty (klucz: user z JWT, fallback IP)
RATE_LIMIT_WRITE = "60/minute"  # zapisy (klucz: user z JWT, fallback IP)


def auth_or_ip_key(request: Request) -> str:
    """Limit per-user na podstawie claimu `id` z JWT (bez weryfikacji podpisu -
    to tylko klucz limitera, autoryzację robi middleware), fallback na IP."""
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        try:
            payload = jwt.decode(auth_header[7:], options={"verify_signature": False})
            user_id = payload.get("id")
            if user_id:
                return f"user:{user_id}"
        except jwt.InvalidTokenError:
            pass
    return get_remote_address(request)


# Storage in-memory (projekt nie ma Redisa) - limity liczone per worker gunicorna.
# Po ewentualnym dodaniu Redisa podać storage_uri, żeby limity były wspólne
# dla wszystkich replik (jak w docs/ARCHITEKTURA.md 7.4).
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200/second"],
)


def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    error = ApiErrorData(
        message=f"Rate limit exceeded: {exc.detail}",
        type_module="rate_limit_exceeded_handler",
        type_error="rate_limit_exceeded",
        key_type_error="Exception",
    )
    return JSONResponse(status_code=429, content=ApiErrorResponse(status_code=429, data=error).model_dump())
