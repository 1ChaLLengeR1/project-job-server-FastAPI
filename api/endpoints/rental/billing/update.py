from dataclasses import asdict

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, ApiResponse
from api.routers import UPDATE_RENTAL_METER_READING, UPDATE_RENTAL_PERIOD
from api.schemas.rental.billing.payload import (
    RentalBillingPeriodUpdatePayload,
    RentalMeterReadingUpdatePayload,
)
from api.schemas.rental.billing.response import (
    RentalBillingPeriodResponseData,
    RentalMeterReadingResponseData,
)
from api.validators import is_valid_uuid
from config.rate_limit import RATE_LIMIT_WRITE, auth_or_ip_key, limiter
from core.data.user import UserData
from core.handler.rental.billing.update import (
    handler_update_billing_period,
    handler_update_meter_reading,
)
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from database.psql.database import get_db

router = APIRouter()


def _invalid_uuid_response(field_name: str, type_module: str) -> JSONResponse:
    error = ApiErrorData(
        message=f"{field_name} nie jest poprawnego formatu uuid.",
        type_module=type_module,
        type_error="validation_error",
        key_type_error="Exception",
    )
    return JSONResponse(status_code=400, content=ApiErrorResponse(status_code=400, data=error).model_dump())


@router.put(
    UPDATE_RENTAL_PERIOD,
    summary="[Superadmin] Zaktualizuj okres rozliczeniowy (kwoty rachunku / stawki)",
    description="Korekta kwoty rachunku prądu, stawek i notatki. Zamknięty okres wymaga wcześniejszego reopen.",
    response_model=ApiResponse[RentalBillingPeriodResponseData],
    responses={
        400: {"model": ApiErrorResponse, "description": "Niepoprawny format period_id"},
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        404: {"model": ApiErrorResponse, "description": "Okres nie istnieje"},
        409: {"model": ApiErrorResponse, "description": "Okres jest zamknięty"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["Rentals/Billing"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_superadmin_update_rental_period(
    request: Request,
    period_id: str,
    body: RentalBillingPeriodUpdatePayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[RentalBillingPeriodResponseData] | JSONResponse:
    try:
        if not is_valid_uuid(period_id):
            return _invalid_uuid_response("Period_id", "api_superadmin_update_rental_period")

        data, error, success = handler_update_billing_period(
            user_data["id"],
            period_id,
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

        return ApiResponse(status="SUCCESS", status_code=200, data=RentalBillingPeriodResponseData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_update_rental_period",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())


@router.put(
    UPDATE_RENTAL_METER_READING,
    summary="[Superadmin] Zaktualizuj odczyt licznika",
    description="Wpisanie odczytu 'Teraz' i ewentualnej ręcznej korekty błędu licznika.",
    response_model=ApiResponse[RentalMeterReadingResponseData],
    responses={
        400: {"model": ApiErrorResponse, "description": "Niepoprawny format reading_id"},
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        404: {"model": ApiErrorResponse, "description": "Odczyt nie istnieje"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["Rentals/Billing"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_superadmin_update_rental_meter_reading(
    request: Request,
    reading_id: str,
    body: RentalMeterReadingUpdatePayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[RentalMeterReadingResponseData] | JSONResponse:
    try:
        if not is_valid_uuid(reading_id):
            return _invalid_uuid_response("Reading_id", "api_superadmin_update_rental_meter_reading")

        data, error, success = handler_update_meter_reading(
            user_data["id"],
            reading_id,
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

        return ApiResponse(status="SUCCESS", status_code=200, data=RentalMeterReadingResponseData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_update_rental_meter_reading",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())
