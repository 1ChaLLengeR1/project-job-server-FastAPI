from dataclasses import asdict

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, ApiResponse
from api.routers import COLLECTION_FILES_NODES
from api.schemas.file.node.response import FilesNodeResponseData
from api.validators import is_valid_uuid
from config.rate_limit import RATE_LIMIT_READ, auth_or_ip_key, limiter
from core.data.user import UserData
from core.handler.file.node.collection import handler_collection_files_nodes
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from database.psql.database import get_db

router = APIRouter()


@router.get(
    COLLECTION_FILES_NODES,
    summary="[Superadmin] Pobierz listę węzłów (dzieci danego węzła)",
    response_model=ApiResponse[list[FilesNodeResponseData]],
    responses={
        400: {"model": ApiErrorResponse, "description": "Niepoprawny format parent_id"},
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["Files/Nodes"],
)
@limiter.limit(RATE_LIMIT_READ, key_func=auth_or_ip_key)
def api_superadmin_collection_files_nodes(
    request: Request,
    parent_id: str | None = Query(
        default=None, description="UUID węzła nadrzędnego; pominięcie = węzły najwyższego poziomu"
    ),
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[list[FilesNodeResponseData]] | JSONResponse:
    try:
        if parent_id is not None and not is_valid_uuid(parent_id):
            error = ApiErrorData(
                message="Parent_id nie jest poprawnego formatu uuid.",
                type_module="api_superadmin_collection_files_nodes",
                type_error="validation_error",
                key_type_error="Exception",
            )
            return JSONResponse(status_code=400, content=ApiErrorResponse(status_code=400, data=error).model_dump())

        data, error, success = handler_collection_files_nodes(user_data["id"], parent_id, db_session=db)
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(
            status="SUCCESS", status_code=200, data=[FilesNodeResponseData(**asdict(node)) for node in data]
        )
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_collection_files_nodes",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())
