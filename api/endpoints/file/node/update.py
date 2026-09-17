from dataclasses import asdict

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, ApiResponse
from api.routers import UPDATE_FILES_NODE
from api.schemas.file.node.payload import FilesNodeUpdatePayload
from api.schemas.file.node.response import FilesNodeResponseData
from api.validators import is_valid_uuid
from config.rate_limit import RATE_LIMIT_WRITE, auth_or_ip_key, limiter
from core.data.user import UserData
from core.handler.file.node.update import handler_update_files_node
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from database.psql.database import get_db

router = APIRouter()


@router.put(
    UPDATE_FILES_NODE,
    summary="[Superadmin] Zaktualizuj węzeł (nazwa/opis/rodzic/aktywność)",
    response_model=ApiResponse[FilesNodeResponseData],
    responses={
        400: {"model": ApiErrorResponse, "description": "Niepoprawny format node_id"},
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        404: {"model": ApiErrorResponse, "description": "Węzeł nie istnieje"},
        409: {"model": ApiErrorResponse, "description": "Konflikt danych (IntegrityError)"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["Files/Nodes"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_superadmin_update_files_node(
    request: Request,
    node_id: str,
    body: FilesNodeUpdatePayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[FilesNodeResponseData] | JSONResponse:
    try:
        if not is_valid_uuid(node_id):
            error = ApiErrorData(
                message="Node_id nie jest poprawnego formatu uuid.",
                type_module="api_superadmin_update_files_node",
                type_error="validation_error",
                key_type_error="Exception",
            )
            return JSONResponse(status_code=400, content=ApiErrorResponse(status_code=400, data=error).model_dump())

        # Jawne `parent_id: null` w body przenosi węzeł na najwyższy poziom; brak klucza
        # `parent_id` w body = nie dotykaj rodzica. Oba przypadki dają `body.parent_id is None`,
        # więc rozróżnienie idzie po `model_fields_set`.
        parent_id_provided = "parent_id" in body.model_fields_set
        clear_parent_id = parent_id_provided and body.parent_id is None

        data, error, success = handler_update_files_node(
            user_data["id"],
            node_id,
            new_name=body.name,
            new_description=body.description,
            new_parent_id=body.parent_id,
            clear_parent_id=clear_parent_id,
            new_is_active=body.is_active,
            db_session=db,
        )
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=200, data=FilesNodeResponseData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_update_files_node",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())
