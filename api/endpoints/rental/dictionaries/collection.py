from dataclasses import asdict
from datetime import date
from typing import Literal

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, ApiResponse
from api.routers import (
    COLLECTION_RENTAL_APARTMENT_COSTS,
    COLLECTION_RENTAL_APARTMENTS,
    COLLECTION_RENTAL_COST_TYPES,
    COLLECTION_RENTAL_METERS,
    COLLECTION_RENTAL_TENANCIES,
    COLLECTION_RENTAL_TENANTS,
)
from api.schemas.rental.dictionaries.response import (
    RentalApartmentCostResponseData,
    RentalApartmentResponseData,
    RentalCostTypeResponseData,
    RentalMeterResponseData,
    RentalTenancyResponseData,
    RentalTenantResponseData,
)
from api.validators import is_valid_uuid
from config.rate_limit import RATE_LIMIT_READ, auth_or_ip_key, limiter
from core.data.user import UserData
from core.handler.rental.dictionaries.collection import (
    handler_collection_apartment_costs,
    handler_collection_apartments,
    handler_collection_cost_types,
    handler_collection_meters,
    handler_collection_tenancies,
    handler_collection_tenants,
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
    COLLECTION_RENTAL_APARTMENTS,
    summary="[Superadmin] Pobierz listę mieszkań",
    response_model=ApiResponse[list[RentalApartmentResponseData]],
    responses={
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["Rentals/Dictionaries"],
)
@limiter.limit(RATE_LIMIT_READ, key_func=auth_or_ip_key)
def api_superadmin_collection_rental_apartments(
    request: Request,
    is_active: bool | None = Query(default=None, description="Filtr aktywności (None = wszystkie)"),
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[list[RentalApartmentResponseData]] | JSONResponse:
    try:
        data, error, success = handler_collection_apartments(user_data["id"], is_active, db_session=db)
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(
            status="SUCCESS", status_code=200, data=[RentalApartmentResponseData(**asdict(item)) for item in data]
        )
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_collection_rental_apartments",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())


@router.get(
    COLLECTION_RENTAL_TENANTS,
    summary="[Superadmin] Pobierz listę najemców",
    response_model=ApiResponse[list[RentalTenantResponseData]],
    responses={
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["Rentals/Dictionaries"],
)
@limiter.limit(RATE_LIMIT_READ, key_func=auth_or_ip_key)
def api_superadmin_collection_rental_tenants(
    request: Request,
    is_active: bool | None = Query(default=None, description="Filtr aktywności (None = wszystkie)"),
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[list[RentalTenantResponseData]] | JSONResponse:
    try:
        data, error, success = handler_collection_tenants(user_data["id"], is_active, db_session=db)
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(
            status="SUCCESS", status_code=200, data=[RentalTenantResponseData(**asdict(item)) for item in data]
        )
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_collection_rental_tenants",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())


@router.get(
    COLLECTION_RENTAL_TENANCIES,
    summary="[Superadmin] Pobierz listę najmów (z historią)",
    response_model=ApiResponse[list[RentalTenancyResponseData]],
    responses={
        400: {"model": ApiErrorResponse, "description": "Niepoprawny format apartment_id lub tenant_id"},
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["Rentals/Dictionaries"],
)
@limiter.limit(RATE_LIMIT_READ, key_func=auth_or_ip_key)
def api_superadmin_collection_rental_tenancies(
    request: Request,
    apartment_id: str | None = Query(default=None, description="Filtr po mieszkaniu (UUID)"),
    tenant_id: str | None = Query(default=None, description="Filtr po najemcy (UUID)"),
    active_on: date | None = Query(default=None, description="Tylko najmy aktywne w danym dniu"),
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[list[RentalTenancyResponseData]] | JSONResponse:
    try:
        if apartment_id is not None and not is_valid_uuid(apartment_id):
            return _invalid_uuid_response("Apartment_id", "api_superadmin_collection_rental_tenancies")
        if tenant_id is not None and not is_valid_uuid(tenant_id):
            return _invalid_uuid_response("Tenant_id", "api_superadmin_collection_rental_tenancies")

        data, error, success = handler_collection_tenancies(
            user_data["id"], apartment_id, tenant_id, active_on, db_session=db
        )
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(
            status="SUCCESS", status_code=200, data=[RentalTenancyResponseData(**asdict(item)) for item in data]
        )
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_collection_rental_tenancies",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())


@router.get(
    COLLECTION_RENTAL_COST_TYPES,
    summary="[Superadmin] Pobierz listę rodzajów kosztów",
    response_model=ApiResponse[list[RentalCostTypeResponseData]],
    responses={
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["Rentals/Dictionaries"],
)
@limiter.limit(RATE_LIMIT_READ, key_func=auth_or_ip_key)
def api_superadmin_collection_rental_cost_types(
    request: Request,
    is_active: bool | None = Query(default=None, description="Filtr aktywności (None = wszystkie)"),
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[list[RentalCostTypeResponseData]] | JSONResponse:
    try:
        data, error, success = handler_collection_cost_types(user_data["id"], is_active, db_session=db)
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(
            status="SUCCESS", status_code=200, data=[RentalCostTypeResponseData(**asdict(item)) for item in data]
        )
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_collection_rental_cost_types",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())


@router.get(
    COLLECTION_RENTAL_APARTMENT_COSTS,
    summary="[Superadmin] Pobierz listę kosztów mieszkań (z historią stawek)",
    response_model=ApiResponse[list[RentalApartmentCostResponseData]],
    responses={
        400: {"model": ApiErrorResponse, "description": "Niepoprawny format apartment_id"},
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["Rentals/Dictionaries"],
)
@limiter.limit(RATE_LIMIT_READ, key_func=auth_or_ip_key)
def api_superadmin_collection_rental_apartment_costs(
    request: Request,
    apartment_id: str | None = Query(default=None, description="Filtr po mieszkaniu (UUID)"),
    active_on: date | None = Query(default=None, description="Tylko koszty obowiązujące w danym dniu"),
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[list[RentalApartmentCostResponseData]] | JSONResponse:
    try:
        if apartment_id is not None and not is_valid_uuid(apartment_id):
            return _invalid_uuid_response("Apartment_id", "api_superadmin_collection_rental_apartment_costs")

        data, error, success = handler_collection_apartment_costs(
            user_data["id"], apartment_id, active_on, db_session=db
        )
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(
            status="SUCCESS", status_code=200, data=[RentalApartmentCostResponseData(**asdict(item)) for item in data]
        )
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_collection_rental_apartment_costs",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())


@router.get(
    COLLECTION_RENTAL_METERS,
    summary="[Superadmin] Pobierz listę liczników",
    response_model=ApiResponse[list[RentalMeterResponseData]],
    responses={
        400: {"model": ApiErrorResponse, "description": "Niepoprawny format apartment_id"},
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["Rentals/Dictionaries"],
)
@limiter.limit(RATE_LIMIT_READ, key_func=auth_or_ip_key)
def api_superadmin_collection_rental_meters(
    request: Request,
    apartment_id: str | None = Query(default=None, description="Filtr po mieszkaniu (UUID)"),
    media_type: Literal["electricity", "water"] | None = Query(default=None, description="Filtr po medium"),
    is_active: bool | None = Query(default=None, description="Filtr aktywności (None = wszystkie)"),
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[list[RentalMeterResponseData]] | JSONResponse:
    try:
        if apartment_id is not None and not is_valid_uuid(apartment_id):
            return _invalid_uuid_response("Apartment_id", "api_superadmin_collection_rental_meters")

        data, error, success = handler_collection_meters(
            user_data["id"], apartment_id, media_type, is_active, db_session=db
        )
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(
            status="SUCCESS", status_code=200, data=[RentalMeterResponseData(**asdict(item)) for item in data]
        )
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_collection_rental_meters",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())
