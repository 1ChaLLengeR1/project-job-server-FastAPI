from dataclasses import asdict

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, ApiResponse, invalid_uuid_response
from api.routers import DOWNLOAD_FILE_URL
from api.schemas.file.response import FileUrlResponseData
from api.validators import is_valid_uuid
from config.rate_limit import RATE_LIMIT_READ, auth_or_ip_key, limiter
from core.data.user import UserData
from core.handler.file.download import handler_download_file
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from database.psql.database import get_db

router = APIRouter()


@router.get(
    DOWNLOAD_FILE_URL,
    summary="[Superadmin] Krótkoterminowy presigned URL do pobrania pliku (attachment) - wariant JSON",
    description="To samo co `GET /files/download/{file_id}`, ale bez 302 - zwraca URL wprost w JSON. "
    "Frontend: `fetch()` z `Authorization` podążający za cross-origin redirectem na S3 gubi CORS w "
    "realnej przeglądarce (mimo poprawnych nagłówków server-side) - ten endpoint eliminuje redirect, "
    "klient robi od razu osobny, czysty `fetch(url)` bez dodatkowych nagłówków.",
    response_model=ApiResponse[FileUrlResponseData],
    responses={
        400: {"model": ApiErrorResponse, "description": "Niepoprawny format file_id"},
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        404: {"model": ApiErrorResponse, "description": "Plik nie istnieje"},
        409: {"model": ApiErrorResponse, "description": "Plik nie ma statusu completed/confirmed"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["Files"],
)
@limiter.limit(RATE_LIMIT_READ, key_func=auth_or_ip_key)
def api_superadmin_download_file_url(
    request: Request,
    file_id: str,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[FileUrlResponseData] | JSONResponse:
    try:
        if not is_valid_uuid(file_id):
            return invalid_uuid_response("File_id", "api_superadmin_download_file_url")

        data, error, success = handler_download_file(user_data["id"], file_id, db_session=db)
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=200, data=FileUrlResponseData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_download_file_url",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())
