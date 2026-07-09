import logging
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from prometheus_client import Counter

from api.response import ApiErrorData, ApiErrorResponse
from core.exceptions.exceptions import AppException

logger = logging.getLogger(__name__)

app_exceptions_total = Counter(
    "app_exceptions_total",
    "Liczba wyjątków AppException per typ",
    ["exception_type", "type_module"],
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        request_id = str(uuid.uuid4())
        app_exceptions_total.labels(exception_type=type(exc).__name__, type_module=exc.type_module).inc()
        logger.warning(
            "AppException [%s] %s w %s: %s",
            request_id,
            type(exc).__name__,
            exc.type_module,
            exc.message,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=ApiErrorResponse(
                status_code=exc.status_code,
                data=ApiErrorData(
                    message=exc.message,
                    type_module=exc.type_module,
                    type_error=exc.type_error,
                    key_type_error=exc.key_type_error,
                ),
                additional={"request_id": request_id},
            ).model_dump(),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        request_id = str(uuid.uuid4())
        # pełny traceback do logów, do klienta generyczne 500 bez treści wyjątku
        logger.exception("Nieobsłużony wyjątek [%s] na %s %s", request_id, request.method, request.url.path)
        return JSONResponse(
            status_code=500,
            content=ApiErrorResponse(
                status_code=500,
                data=ApiErrorData(
                    message="Internal server error",
                    type_module="unhandled_exception_handler",
                    type_error="exception",
                    key_type_error="Exception",
                ),
                additional={"request_id": request_id},
            ).model_dump(),
        )
