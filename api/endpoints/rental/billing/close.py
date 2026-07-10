from dataclasses import asdict

from fastapi import APIRouter, Body, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, ApiResponse
from api.routers import CLOSE_RENTAL_PERIOD, REOPEN_RENTAL_PERIOD
from api.schemas.rental.billing.payload import RentalPeriodComputePayload
from api.schemas.rental.billing.response import (
    RentalBillingPeriodResponseData,
    RentalPeriodPreviewResponseData,
)
from api.validators import is_valid_uuid
from config.rate_limit import RATE_LIMIT_WRITE, auth_or_ip_key, limiter
from core.data.user import UserData
from core.handler.rental.billing.close import (
    handler_close_billing_period,
    handler_reopen_billing_period,
)
from core.handler.rental.billing.response import PeriodAdjustmentInput
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from database.psql.database import get_db

router = APIRouter()


def _invalid_uuid_response(type_module: str) -> JSONResponse:
    error = ApiErrorData(
        message="Period_id nie jest poprawnego formatu uuid.",
        type_module=type_module,
        type_error="validation_error",
        key_type_error="Exception",
    )
    return JSONResponse(status_code=400, content=ApiErrorResponse(status_code=400, data=error).model_dump())


@router.post(
    CLOSE_RENTAL_PERIOD,
    summary="[Superadmin] Zamknij okres (zapis snapshotów)",
    description="Wyliczenie + zapis snapshotów: rozliczenia mieszkań z pozycjami i podział rodzinny. "
    "Zamknięty okres nie zmienia się przy późniejszej edycji słowników.",
    response_model=ApiResponse[RentalPeriodPreviewResponseData],
    responses={
        400: {"model": ApiErrorResponse, "description": "Niepoprawny format period_id"},
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        404: {"model": ApiErrorResponse, "description": "Okres nie istnieje"},
        409: {"model": ApiErrorResponse, "description": "Okres jest już zamknięty"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["Rentals/Billing"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_superadmin_close_rental_period(
    request: Request,
    period_id: str,
    body: RentalPeriodComputePayload = Body(default=RentalPeriodComputePayload()),
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[RentalPeriodPreviewResponseData] | JSONResponse:
    try:
        if not is_valid_uuid(period_id):
            return _invalid_uuid_response("api_superadmin_close_rental_period")

        adjustments = [
            PeriodAdjustmentInput(apartment_id=item.apartment_id, name=item.name, amount=item.amount)
            for item in body.adjustments
        ]
        data, error, success = handler_close_billing_period(user_data["id"], period_id, adjustments, db_session=db)
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=200, data=RentalPeriodPreviewResponseData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_close_rental_period",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())


@router.post(
    REOPEN_RENTAL_PERIOD,
    summary="[Superadmin] Otwórz ponownie zamknięty okres",
    description="Kasuje snapshoty rozliczeń, zostawia odczyty i dane wejściowe - okres wraca do draft.",
    response_model=ApiResponse[RentalBillingPeriodResponseData],
    responses={
        400: {"model": ApiErrorResponse, "description": "Niepoprawny format period_id"},
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        404: {"model": ApiErrorResponse, "description": "Okres nie istnieje"},
        409: {"model": ApiErrorResponse, "description": "Okres nie jest zamknięty"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["Rentals/Billing"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_superadmin_reopen_rental_period(
    request: Request,
    period_id: str,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[RentalBillingPeriodResponseData] | JSONResponse:
    try:
        if not is_valid_uuid(period_id):
            return _invalid_uuid_response("api_superadmin_reopen_rental_period")

        data, error, success = handler_reopen_billing_period(user_data["id"], period_id, db_session=db)
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
            type_module="api_superadmin_reopen_rental_period",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())
