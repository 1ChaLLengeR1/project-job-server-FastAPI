from dataclasses import asdict

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, ApiResponse
from api.routers import CREATE_RENTAL_METER_READING, CREATE_RENTAL_PERIOD
from api.schemas.rental.billing.payload import (
    RentalBillingPeriodCreatePayload,
    RentalMeterReadingCreatePayload,
)
from api.schemas.rental.billing.response import (
    RentalBillingPeriodResponseData,
    RentalMeterReadingResponseData,
)
from config.rate_limit import RATE_LIMIT_WRITE, auth_or_ip_key, limiter
from core.data.user import UserData
from core.handler.rental.billing.create import (
    handler_create_billing_period,
    handler_create_meter_reading,
)
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from database.psql.database import get_db

router = APIRouter()


@router.post(
    CREATE_RENTAL_PERIOD,
    summary="[Superadmin] Utwórz okres rozliczeniowy (z prefill odczytów)",
    description="Tworzy nowy okres i szkielet odczytów dla aktywnych liczników - "
    "'Ostatnio' prefillowane z ostatniego okresu danego licznika (0 dla nowego licznika).",
    response_model=ApiResponse[RentalBillingPeriodResponseData],
    responses={
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        409: {"model": ApiErrorResponse, "description": "Okres dla tego miesiąca już istnieje"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=201,
    tags=["Rentals/Billing"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_superadmin_create_rental_period(
    request: Request,
    body: RentalBillingPeriodCreatePayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[RentalBillingPeriodResponseData] | JSONResponse:
    try:
        data, error, success = handler_create_billing_period(
            user_data["id"],
            body.period_month,
            body.electricity_bill_amount,
            body.electricity_rate,
            body.electricity_rate_is_manual,
            body.water_rate,
            body.note,
            db_session=db,
        )
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=201, data=RentalBillingPeriodResponseData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_create_rental_period",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())


@router.post(
    CREATE_RENTAL_METER_READING,
    summary="[Superadmin] Dodaj odczyt licznika w okresie",
    description="Ręczne dodanie odczytu - np. dla licznika założonego po utworzeniu okresu.",
    response_model=ApiResponse[RentalMeterReadingResponseData],
    responses={
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        404: {"model": ApiErrorResponse, "description": "Okres lub licznik nie istnieje"},
        409: {"model": ApiErrorResponse, "description": "Odczyt tego licznika w tym okresie już istnieje"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=201,
    tags=["Rentals/Billing"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_superadmin_create_rental_meter_reading(
    request: Request,
    body: RentalMeterReadingCreatePayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[RentalMeterReadingResponseData] | JSONResponse:
    try:
        data, error, success = handler_create_meter_reading(
            user_data["id"],
            body.period_id,
            body.meter_id,
            body.previous_value,
            body.current_value,
            body.error_correction,
            db_session=db,
        )
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=201, data=RentalMeterReadingResponseData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_create_rental_meter_reading",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())
