from dataclasses import asdict
from typing import Literal

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, ApiResponse
from api.routers import (
    COLLECTION_RENTAL_METER_READINGS,
    COLLECTION_RENTAL_PERIODS,
    COLLECTION_RENTAL_SETTLEMENTS,
)
from api.schemas.rental.billing.response import (
    RentalBillingPeriodResponseData,
    RentalMeterReadingResponseData,
    RentalSettlementResponseData,
)
from api.validators import is_valid_uuid
from config.rate_limit import RATE_LIMIT_READ, auth_or_ip_key, limiter
from core.data.user import UserData
from core.handler.rental.billing.collection import (
    handler_collection_billing_periods,
    handler_collection_meter_readings,
    handler_collection_settlements,
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


@router.get(
    COLLECTION_RENTAL_PERIODS,
    summary="[Superadmin] Pobierz listę okresów rozliczeniowych",
    response_model=ApiResponse[list[RentalBillingPeriodResponseData]],
    responses={
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["Rentals/Billing"],
)
@limiter.limit(RATE_LIMIT_READ, key_func=auth_or_ip_key)
def api_superadmin_collection_rental_periods(
    request: Request,
    status: Literal["draft", "closed"] | None = Query(default=None, description="Filtr statusu okresu"),
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[list[RentalBillingPeriodResponseData]] | JSONResponse:
    try:
        data, error, success = handler_collection_billing_periods(user_data["id"], status, db_session=db)
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(
            status="SUCCESS", status_code=200, data=[RentalBillingPeriodResponseData(**asdict(item)) for item in data]
        )
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_collection_rental_periods",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())


@router.get(
    COLLECTION_RENTAL_METER_READINGS,
    summary="[Superadmin] Pobierz odczyty liczników w okresie",
    response_model=ApiResponse[list[RentalMeterReadingResponseData]],
    responses={
        400: {"model": ApiErrorResponse, "description": "Niepoprawny format period_id"},
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        404: {"model": ApiErrorResponse, "description": "Okres nie istnieje"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["Rentals/Billing"],
)
@limiter.limit(RATE_LIMIT_READ, key_func=auth_or_ip_key)
def api_superadmin_collection_rental_meter_readings(
    request: Request,
    period_id: str,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[list[RentalMeterReadingResponseData]] | JSONResponse:
    try:
        if not is_valid_uuid(period_id):
            return _invalid_uuid_response("Period_id", "api_superadmin_collection_rental_meter_readings")

        data, error, success = handler_collection_meter_readings(user_data["id"], period_id, db_session=db)
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(
            status="SUCCESS", status_code=200, data=[RentalMeterReadingResponseData(**asdict(item)) for item in data]
        )
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_collection_rental_meter_readings",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())


@router.get(
    COLLECTION_RENTAL_SETTLEMENTS,
    summary="[Superadmin] Pobierz snapshoty rozliczeń mieszkań",
    description="Snapshoty zapisane przy zamknięciu okresów - filtrowanie po okresie i/lub mieszkaniu.",
    response_model=ApiResponse[list[RentalSettlementResponseData]],
    responses={
        400: {"model": ApiErrorResponse, "description": "Niepoprawny format period_id lub apartment_id"},
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["Rentals/Billing"],
)
@limiter.limit(RATE_LIMIT_READ, key_func=auth_or_ip_key)
def api_superadmin_collection_rental_settlements(
    request: Request,
    period_id: str | None = Query(default=None, description="Filtr po okresie (UUID)"),
    apartment_id: str | None = Query(default=None, description="Filtr po mieszkaniu (UUID)"),
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[list[RentalSettlementResponseData]] | JSONResponse:
    try:
        if period_id is not None and not is_valid_uuid(period_id):
            return _invalid_uuid_response("Period_id", "api_superadmin_collection_rental_settlements")
        if apartment_id is not None and not is_valid_uuid(apartment_id):
            return _invalid_uuid_response("Apartment_id", "api_superadmin_collection_rental_settlements")

        data, error, success = handler_collection_settlements(user_data["id"], period_id, apartment_id, db_session=db)
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(
            status="SUCCESS", status_code=200, data=[RentalSettlementResponseData(**asdict(item)) for item in data]
        )
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_collection_rental_settlements",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())
