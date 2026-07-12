from dataclasses import asdict

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, ApiResponse
from api.routers import (
    CREATE_RENTAL_APARTMENT,
    CREATE_RENTAL_APARTMENT_COST,
    CREATE_RENTAL_COST_TYPE,
    CREATE_RENTAL_METER,
    CREATE_RENTAL_TENANCY,
    CREATE_RENTAL_TENANT,
)
from api.schemas.rental.dictionaries.payload import (
    RentalApartmentCostCreatePayload,
    RentalApartmentCreatePayload,
    RentalCostTypeCreatePayload,
    RentalMeterCreatePayload,
    RentalTenancyCreatePayload,
    RentalTenantCreatePayload,
)
from api.schemas.rental.dictionaries.response import (
    RentalApartmentCostResponseData,
    RentalApartmentResponseData,
    RentalCostTypeResponseData,
    RentalMeterResponseData,
    RentalTenancyResponseData,
    RentalTenantResponseData,
)
from config.rate_limit import RATE_LIMIT_WRITE, auth_or_ip_key, limiter
from core.data.user import UserData
from core.handler.rental.dictionaries.create import (
    handler_create_apartment,
    handler_create_apartment_cost,
    handler_create_cost_type,
    handler_create_meter,
    handler_create_tenancy,
    handler_create_tenant,
)
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from database.psql.database import get_db

router = APIRouter()


@router.post(
    CREATE_RENTAL_APARTMENT,
    summary="[Superadmin] Utwórz mieszkanie",
    response_model=ApiResponse[RentalApartmentResponseData],
    responses={
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        409: {"model": ApiErrorResponse, "description": "Konflikt danych (IntegrityError)"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=201,
    tags=["Rentals/Dictionaries"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_superadmin_create_rental_apartment(
    request: Request,
    body: RentalApartmentCreatePayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[RentalApartmentResponseData] | JSONResponse:
    try:
        data, error, success = handler_create_apartment(
            user_data["id"], body.name, body.description, body.is_active, db_session=db
        )
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=201, data=RentalApartmentResponseData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_create_rental_apartment",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())


@router.post(
    CREATE_RENTAL_TENANT,
    summary="[Superadmin] Utwórz najemcę",
    response_model=ApiResponse[RentalTenantResponseData],
    responses={
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        409: {"model": ApiErrorResponse, "description": "Konflikt danych (IntegrityError)"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=201,
    tags=["Rentals/Dictionaries"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_superadmin_create_rental_tenant(
    request: Request,
    body: RentalTenantCreatePayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[RentalTenantResponseData] | JSONResponse:
    try:
        data, error, success = handler_create_tenant(
            user_data["id"], body.first_name, body.last_name, body.note, body.is_active, db_session=db
        )
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=201, data=RentalTenantResponseData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_create_rental_tenant",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())


@router.post(
    CREATE_RENTAL_TENANCY,
    summary="[Superadmin] Utwórz najem (najemca + mieszkanie + czynsz)",
    response_model=ApiResponse[RentalTenancyResponseData],
    responses={
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        404: {"model": ApiErrorResponse, "description": "Mieszkanie lub najemca nie istnieje"},
        409: {"model": ApiErrorResponse, "description": "Konflikt danych (np. nakładające się najmy)"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=201,
    tags=["Rentals/Dictionaries"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_superadmin_create_rental_tenancy(
    request: Request,
    body: RentalTenancyCreatePayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[RentalTenancyResponseData] | JSONResponse:
    try:
        data, error, success = handler_create_tenancy(
            user_data["id"],
            body.apartment_id,
            body.tenant_id,
            body.rent_amount,
            body.persons_count,
            body.start_date,
            body.end_date,
            db_session=db,
        )
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=201, data=RentalTenancyResponseData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_create_rental_tenancy",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())


@router.post(
    CREATE_RENTAL_COST_TYPE,
    summary="[Superadmin] Utwórz rodzaj kosztu",
    response_model=ApiResponse[RentalCostTypeResponseData],
    responses={
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        409: {"model": ApiErrorResponse, "description": "Konflikt danych (IntegrityError)"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=201,
    tags=["Rentals/Dictionaries"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_superadmin_create_rental_cost_type(
    request: Request,
    body: RentalCostTypeCreatePayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[RentalCostTypeResponseData] | JSONResponse:
    try:
        data, error, success = handler_create_cost_type(
            user_data["id"], body.name, body.charge_type, body.is_active, db_session=db
        )
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=201, data=RentalCostTypeResponseData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_create_rental_cost_type",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())


@router.post(
    CREATE_RENTAL_APARTMENT_COST,
    summary="[Superadmin] Przypisz koszt do mieszkania",
    response_model=ApiResponse[RentalApartmentCostResponseData],
    responses={
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        404: {"model": ApiErrorResponse, "description": "Mieszkanie lub rodzaj kosztu nie istnieje"},
        409: {"model": ApiErrorResponse, "description": "Konflikt danych (IntegrityError)"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=201,
    tags=["Rentals/Dictionaries"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_superadmin_create_rental_apartment_cost(
    request: Request,
    body: RentalApartmentCostCreatePayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[RentalApartmentCostResponseData] | JSONResponse:
    try:
        data, error, success = handler_create_apartment_cost(
            user_data["id"],
            body.apartment_id,
            body.cost_type_id,
            body.amount,
            body.start_date,
            body.end_date,
            db_session=db,
        )
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=201, data=RentalApartmentCostResponseData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_create_rental_apartment_cost",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())


@router.post(
    CREATE_RENTAL_METER,
    summary="[Superadmin] Utwórz licznik",
    response_model=ApiResponse[RentalMeterResponseData],
    responses={
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        404: {"model": ApiErrorResponse, "description": "Mieszkanie nie istnieje"},
        409: {"model": ApiErrorResponse, "description": "Konflikt danych (IntegrityError)"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=201,
    tags=["Rentals/Dictionaries"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_superadmin_create_rental_meter(
    request: Request,
    body: RentalMeterCreatePayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[RentalMeterResponseData] | JSONResponse:
    try:
        data, error, success = handler_create_meter(
            user_data["id"],
            body.media_type,
            body.apartment_id,
            body.is_master,
            body.name,
            body.is_active,
            db_session=db,
        )
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=201, data=RentalMeterResponseData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_create_rental_meter",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())
