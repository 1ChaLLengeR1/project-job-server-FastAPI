from dataclasses import asdict

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, ApiResponse
from api.routers import COLLECTION_OUTSTANDING_MONEY
from api.schemas.outstanding_money.response import OverdueListData
from config.rate_limit import RATE_LIMIT_READ, auth_or_ip_key, limiter
from core.data.user import UserData
from core.handler.outstanding_money.collection import handler_collection_list
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from database.psql.database import get_db

router = APIRouter()


@router.get(
    COLLECTION_OUTSTANDING_MONEY,
    summary="[User] Pobierz listy zaległych płatności",
    response_model=ApiResponse[list[OverdueListData]],
    responses={
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["OutstandingMoney"],
)
@limiter.limit(RATE_LIMIT_READ, key_func=auth_or_ip_key)
def api_user_collection_outstanding_money(
    request: Request,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware()),
    db: Session = Depends(get_db),
) -> ApiResponse[list[OverdueListData]] | JSONResponse:
    try:
        data, error, success = handler_collection_list(user_data["id"], db_session=db)
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(
            status="SUCCESS", status_code=200, data=[OverdueListData(**asdict(overdue)) for overdue in data]
        )
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_user_collection_outstanding_money",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())
