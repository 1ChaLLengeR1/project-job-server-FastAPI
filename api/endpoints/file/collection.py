from dataclasses import asdict
from datetime import date
from typing import Literal

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, ApiResponse, invalid_uuid_response
from api.routers import COLLECTION_FILES
from api.schemas.file.response import FileCollectionResponseData
from api.validators import is_valid_uuid
from config.rate_limit import RATE_LIMIT_READ, auth_or_ip_key, limiter
from core.data.user import UserData
from core.handler.file.collection import handler_collection_file
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from database.psql.database import get_db
from database.psql.models.file import FileStatus, FileType

router = APIRouter()


@router.get(
    COLLECTION_FILES,
    summary="[Superadmin] Pobierz listę plików",
    description="Bez filtrów zwraca wszystkie pliki niezależnie od statusu/przypisania. "
    "`status` filtruje po statusie (`pending`/`completed`/`failed`/`confirmed` — `completed` ~ "
    "nieprzypisany, `confirmed` ~ przypisany do węzła, patrz `node_id`).",
    response_model=ApiResponse[FileCollectionResponseData],
    responses={
        400: {"model": ApiErrorResponse, "description": "Niepoprawny format node_id"},
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["Files"],
)
@limiter.limit(RATE_LIMIT_READ, key_func=auth_or_ip_key)
def api_superadmin_collection_files(
    request: Request,
    limit: int = Query(default=32, gt=0, le=200, description="Liczba wyników na stronę"),
    offset: int = Query(default=0, ge=0, description="Przesunięcie od początku listy"),
    file_type: FileType | None = Query(default=None, description="Filtr po typie pliku"),
    status: FileStatus | None = Query(default=None, description="Filtr po statusie pliku"),
    original_name: str | None = Query(default=None, description="Filtr ILIKE po nazwie wyświetlanej"),
    catalog: str | None = Query(default=None, description="Filtr po prefiksie/katalogu S3"),
    node_id: str | None = Query(default=None, description="Filtr po węźle (UUID)"),
    recursive: bool = Query(
        default=False, description="Z node_id: dołącz pliki z całego poddrzewa węzła, nie tylko wprost pod nim"
    ),
    created_at_from: date | None = Query(default=None, description="Tylko pliki dodane od tej daty (włącznie)"),
    created_at_to: date | None = Query(default=None, description="Tylko pliki dodane do tej daty (włącznie)"),
    guarantee_status: Literal["active", "expired", "none"] | None = Query(
        default=None, description="Filtr po statusie gwarancji względem guarantee_end_date"
    ),
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[FileCollectionResponseData] | JSONResponse:
    try:
        if node_id is not None and not is_valid_uuid(node_id):
            return invalid_uuid_response("Node_id", "api_superadmin_collection_files")

        data, error, success = handler_collection_file(
            user_data["id"],
            limit=limit,
            offset=offset,
            file_type=file_type,
            status=status,
            original_name=original_name,
            catalog=catalog,
            node_id=node_id,
            recursive=recursive,
            created_at_from=created_at_from,
            created_at_to=created_at_to,
            guarantee_status=guarantee_status,
            db_session=db,
        )
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=200, data=FileCollectionResponseData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_collection_files",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())
