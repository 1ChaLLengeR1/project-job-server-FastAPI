from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.requests import Request

# Storage in-memory (projekt nie ma Redisa) - limity liczone per worker gunicorna.
# Po ewentualnym dodaniu Redisa podać storage_uri, żeby limity były wspólne
# dla wszystkich replik (jak w docs/ARCHITEKTURA.md 7.4).
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200/second"],
)


def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    return JSONResponse(
        status_code=429,
        content={
            "status": "ERROR",
            "status_code": 429,
            "data": {"message": f"Rate limit exceeded: {exc.detail}"},
            "additional": None,
        },
    )
