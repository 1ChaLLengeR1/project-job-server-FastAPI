from dataclasses import asdict

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, ApiResponse
from api.routers import ONE_RENTAL_PERIOD, ONE_RENTAL_SETTLEMENT
from api.schemas.rental.billing.response import (
    RentalBillingPeriodResponseData,
    RentalSettlementResponseData,
)
from api.validators import is_valid_uuid
from config.rate_limit import RATE_LIMIT_READ, auth_or_ip_key, limiter
from core.data.user import UserData
from core.handler.rental.billing.one import handler_one_billing_period, handler_one_settlement
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from database.psql.database import get_db

router = APIRouter()

_ONE_RESPONSES = {
    400: {"model": ApiErrorResponse, "description": "Niepoprawny format identyfikatora"},
    401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
    403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
    404: {"model": ApiErrorResponse, "description": "Rekord nie istnieje"},
    429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
    500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
}


def _invalid_uuid_response(field_name: str, type_module: str) -> JSONResponse:
    error = ApiErrorData(
        message=f"{field_name} nie jest poprawnego formatu uuid.",
        type_module=type_module,
        type_error="validation_error",
        key_type_error="Exception",
    )
    return JSONResponse(status_code=400, content=ApiErrorResponse(status_code=400, data=error).model_dump())


@router.get(
    ONE_RENTAL_PERIOD,
    summary="[Superadmin] Pobierz okres rozliczeniowy",
    response_model=ApiResponse[RentalBillingPeriodResponseData],
    responses=_ONE_RESPONSES,
    status_code=200,
    tags=["Rentals/Billing"],
)
@limiter.limit(RATE_LIMIT_READ, key_func=auth_or_ip_key)
def api_superadmin_one_rental_period(
    request: Request,
    period_id: str,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[RentalBillingPeriodResponseData] | JSONResponse:
    try:
        if not is_valid_uuid(period_id):
            return _invalid_uuid_response("Period_id", "api_superadmin_one_rental_period")

        data, error, success = handler_one_billing_period(user_data["id"], period_id, db_session=db)
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=200, data=RentalBillingPeriodResponseData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_one_rental_period",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())


@router.get(
    ONE_RENTAL_SETTLEMENT,
    summary="[Superadmin] Pobierz snapshot rozliczenia mieszkania",
    response_model=ApiResponse[RentalSettlementResponseData],
    responses=_ONE_RESPONSES,
    status_code=200,
    tags=["Rentals/Billing"],
)
@limiter.limit(RATE_LIMIT_READ, key_func=auth_or_ip_key)
def api_superadmin_one_rental_settlement(
    request: Request,
    settlement_id: str,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[RentalSettlementResponseData] | JSONResponse:
    try:
        if not is_valid_uuid(settlement_id):
            return _invalid_uuid_response("Settlement_id", "api_superadmin_one_rental_settlement")

        data, error, success = handler_one_settlement(user_data["id"], settlement_id, db_session=db)
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=200, data=RentalSettlementResponseData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_one_rental_settlement",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())
