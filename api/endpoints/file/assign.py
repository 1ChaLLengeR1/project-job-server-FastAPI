from dataclasses import asdict

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, ApiResponse, invalid_uuid_response
from api.routers import ASSIGN_FILE
from api.schemas.file.payload import FileAssignPayload
from api.schemas.file.response import FileResponseData
from api.validators import is_valid_uuid
from config.rate_limit import RATE_LIMIT_WRITE, auth_or_ip_key, limiter
from core.data.user import UserData
from core.handler.file.assign import handler_assign_file
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from database.psql.database import get_db

router = APIRouter()


@router.put(
    ASSIGN_FILE,
    summary="[Superadmin] Przypisz plik do węzła (COMPLETED -> CONFIRMED)",
    response_model=ApiResponse[FileResponseData],
    responses={
        400: {"model": ApiErrorResponse, "description": "Niepoprawny format file_id"},
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        404: {"model": ApiErrorResponse, "description": "Plik nie istnieje"},
        409: {
            "model": ApiErrorResponse,
            "description": "Plik nie ma statusu completed, lub konflikt danych (IntegrityError)",
        },
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["Files"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_superadmin_assign_file(
    request: Request,
    file_id: str,
    body: FileAssignPayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[FileResponseData] | JSONResponse:
    try:
        if not is_valid_uuid(file_id):
            return invalid_uuid_response("File_id", "api_superadmin_assign_file")

        data, error, success = handler_assign_file(
            user_data["id"], file_id, body.node_id, body.parent_file_id, db_session=db
        )
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=200, data=FileResponseData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_assign_file",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())
