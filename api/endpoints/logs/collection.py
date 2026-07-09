from dataclasses import asdict

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, ApiResponse
from api.routers import COLLECTION_LOGS
from api.schemas.logs.response import LogResponseData
from core.handler.logs.collection import handler_collection_logs
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from database.psql.database import get_db

router = APIRouter()


@router.get(
    COLLECTION_LOGS,
    summary="[Superadmin] Pobierz logi audytowe",
    response_model=ApiResponse[list[LogResponseData]],
    responses={
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["Logs"],
    dependencies=[Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"]))],
)
def api_superadmin_collection_logs(
    number: int,
    db: Session = Depends(get_db),
) -> ApiResponse[list[LogResponseData]] | JSONResponse:
    try:
        data, error, success = handler_collection_logs(number, db_session=db)
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=200, data=[LogResponseData(**asdict(log)) for log in data])
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_collection_logs",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())
