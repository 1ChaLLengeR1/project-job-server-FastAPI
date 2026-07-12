from dataclasses import asdict

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, ApiResponse
from api.routers import CALCULATOR_KEYS_UPDATE
from api.schemas.patryk_router.payload import KeysCalculatorUpdatePayload
from api.schemas.patryk_router.response import KeysCalculatorResponseData
from config.rate_limit import RATE_LIMIT_WRITE, auth_or_ip_key, limiter
from core.data.user import UserData
from core.handler.patryk.calculator_work.update import handler_update_calculator_keys
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from database.psql.database import get_db

router = APIRouter()


@router.put(
    CALCULATOR_KEYS_UPDATE,
    summary="[Admin] Zaktualizuj klucze kalkulatora",
    response_model=ApiResponse[KeysCalculatorResponseData],
    responses={
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola admin)"},
        404: {"model": ApiErrorResponse, "description": "Nie znaleziono rekordu kluczy o podanym id"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["Patryk/Calculator"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_admin_update_calculator_keys(
    request: Request,
    body: KeysCalculatorUpdatePayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["admin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[KeysCalculatorResponseData] | JSONResponse:
    try:
        data, error, success = handler_update_calculator_keys(
            user_data["id"],
            body.id,
            body.income_tax,
            body.vat,
            body.inpost_parcel_locker,
            body.inpost_courier,
            body.inpost_cash_of_delivery_courier,
            body.dpd,
            body.allegro_matt,
            body.without_smart,
            db_session=db,
        )
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=200, data=KeysCalculatorResponseData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_admin_update_calculator_keys",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())
