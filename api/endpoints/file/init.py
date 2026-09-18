from dataclasses import asdict

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, ApiResponse
from api.routers import INIT_FILE
from api.schemas.file.payload import FileInitPayload
from api.schemas.file.response import FileInitResponseData
from config.rate_limit import RATE_LIMIT_WRITE, auth_or_ip_key, limiter
from core.data.user import UserData
from core.handler.file.init import handler_init_upload_file
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from database.psql.database import get_db

router = APIRouter()


@router.post(
    INIT_FILE,
    summary="[Superadmin] Zainicjuj upload pliku (presigned PUT do S3)",
    description="Rozmiar pliku (`size`) ograniczony do 50 MB. Response niesie `kms_key_id` "
    "obok `signed_url` — PUT na `signed_url` musi wysłać dokładnie nagłówki "
    "`x-amz-server-side-encryption: aws:kms` i "
    "`x-amz-server-side-encryption-aws-kms-key-id: {kms_key_id}`, inaczej S3 zwróci "
    "`403 SignatureDoesNotMatch` (nie AccessDenied).",
    response_model=ApiResponse[FileInitResponseData],
    responses={
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        409: {"model": ApiErrorResponse, "description": "Konflikt danych (IntegrityError)"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=201,
    tags=["Files"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_superadmin_init_file(
    request: Request,
    body: FileInitPayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[FileInitResponseData] | JSONResponse:
    try:
        data, error, success = handler_init_upload_file(
            user_data["id"],
            body.name,
            body.original_name,
            body.size,
            body.file_type,
            body.mime_type,
            body.catalog,
            db_session=db,
        )
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=201, data=FileInitResponseData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_init_file",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())
