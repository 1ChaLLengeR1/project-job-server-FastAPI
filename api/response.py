from typing import Any, Generic, Literal

from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing_extensions import TypeVar

DATA = TypeVar("DATA", default=Any)
ADDITIONALS = TypeVar("ADDITIONALS", default=Any)

# Mapowanie key_type_error -> HTTP status (konwencja z ARCHITEKTURA.md, sekcja 4.1)
ERROR_STATUS_CODES = {
    "IntegrityError": 409,
    "NotFound": 404,
    "Forbidden": 403,
    "Unauthorized": 401,
    "ExternalService": 502,
}


class ApiResponse(BaseModel, Generic[DATA, ADDITIONALS]):
    status: Literal["SUCCESS", "ERROR"]
    status_code: int
    data: DATA | None = None
    additional: ADDITIONALS | None = None


class ApiErrorData(BaseModel):
    message: str
    type_module: str  # nazwa funkcji, w której powstał błąd, np. "create_task_psql"
    type_error: str
    key_type_error: str  # "IntegrityError" (409) | "NotFound" (404) | "Exception" (400/500)


class ApiErrorResponse(BaseModel, Generic[ADDITIONALS]):
    status: Literal["ERROR"] = "ERROR"
    status_code: int
    data: ApiErrorData
    additional: ADDITIONALS | None = None


def invalid_uuid_response(field_name: str, type_module: str) -> JSONResponse:
    """Wspolna odpowiedz 400 dla niepoprawnego formatu UUID w path/query param -
    wczesniej kopiowana (lokalnie jako `_invalid_uuid_response` albo inline)
    niemal identycznie w kilkudziesieciu plikach `api/endpoints/`."""
    error = ApiErrorData(
        message=f"{field_name} nie jest poprawnego formatu uuid.",
        type_module=type_module,
        type_error="validation_error",
        key_type_error="Exception",
    )
    return JSONResponse(status_code=400, content=ApiErrorResponse(status_code=400, data=error).model_dump())
