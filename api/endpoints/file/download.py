from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, invalid_uuid_response
from api.routers import DOWNLOAD_FILE
from api.validators import is_valid_uuid
from config.rate_limit import RATE_LIMIT_READ, auth_or_ip_key, limiter
from core.data.user import UserData
from core.handler.file.download import handler_download_file
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from database.psql.database import get_db

router = APIRouter()


@router.get(
    DOWNLOAD_FILE,
    summary="[Superadmin] Pobierz plik (302 -> krótkoterminowy presigned URL, attachment)",
    response_model=None,
    responses={
        302: {"description": "Redirect na presigned URL S3 z Content-Disposition: attachment"},
        400: {"model": ApiErrorResponse, "description": "Niepoprawny format file_id"},
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        404: {"model": ApiErrorResponse, "description": "Plik nie istnieje"},
        409: {"model": ApiErrorResponse, "description": "Plik nie ma statusu completed/confirmed"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=302,
    tags=["Files"],
)
@limiter.limit(RATE_LIMIT_READ, key_func=auth_or_ip_key)
def api_superadmin_download_file(
    request: Request,
    file_id: str,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> RedirectResponse | JSONResponse:
    try:
        if not is_valid_uuid(file_id):
            return invalid_uuid_response("File_id", "api_superadmin_download_file")

        data, error, success = handler_download_file(user_data["id"], file_id, db_session=db)
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return RedirectResponse(url=data.url, status_code=302)
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_download_file",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())
