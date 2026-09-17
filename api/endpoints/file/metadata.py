from dataclasses import asdict

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, ApiResponse, invalid_uuid_response
from api.routers import UPDATE_FILE_METADATA
from api.schemas.file.payload import FileMetadataPayload
from api.schemas.file.response import FileResponseData
from api.validators import is_valid_uuid
from config.rate_limit import RATE_LIMIT_WRITE, auth_or_ip_key, limiter
from core.data.user import UserData
from core.handler.file.metadata import handler_update_file_metadata
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from database.psql.database import get_db

router = APIRouter()


@router.put(
    UPDATE_FILE_METADATA,
    summary="[Superadmin] Edytuj metadane pliku (nazwa/węzeł/rodzic/opis/gwarancja)",
    response_model=ApiResponse[FileResponseData],
    responses={
        400: {"model": ApiErrorResponse, "description": "Niepoprawny format file_id"},
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        404: {"model": ApiErrorResponse, "description": "Plik nie istnieje"},
        409: {"model": ApiErrorResponse, "description": "Konflikt danych (IntegrityError)"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["Files"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_superadmin_update_file_metadata(
    request: Request,
    file_id: str,
    body: FileMetadataPayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[FileResponseData] | JSONResponse:
    try:
        if not is_valid_uuid(file_id):
            return invalid_uuid_response("File_id", "api_superadmin_update_file_metadata")

        # Jawne `null` dla parent_file_id/description/dat gwarancji je czysci; brak klucza
        # w body = nie dotykaj. Oba przypadki daja `None` w Pythonie, wiec rozroznienie
        # idzie po `model_fields_set` (ten sam trick co przy PUT /files/nodes/update).
        fields_set = body.model_fields_set
        clear_parent_file_id = "parent_file_id" in fields_set and body.parent_file_id is None
        clear_description = "description" in fields_set and body.description is None
        clear_guarantee_start_date = "guarantee_start_date" in fields_set and body.guarantee_start_date is None
        clear_guarantee_end_date = "guarantee_end_date" in fields_set and body.guarantee_end_date is None

        data, error, success = handler_update_file_metadata(
            user_data["id"],
            file_id,
            new_original_name=body.original_name,
            new_node_id=body.node_id,
            new_parent_file_id=body.parent_file_id,
            clear_parent_file_id=clear_parent_file_id,
            new_description=body.description,
            clear_description=clear_description,
            new_guarantee_start_date=body.guarantee_start_date,
            clear_guarantee_start_date=clear_guarantee_start_date,
            new_guarantee_end_date=body.guarantee_end_date,
            clear_guarantee_end_date=clear_guarantee_end_date,
            db_session=db,
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
            type_module="api_superadmin_update_file_metadata",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())
