from dataclasses import asdict

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, ApiResponse
from api.routers import (
    UPDATE_RENTAL_APARTMENT,
    UPDATE_RENTAL_APARTMENT_COST,
    UPDATE_RENTAL_COST_TYPE,
    UPDATE_RENTAL_METER,
    UPDATE_RENTAL_TENANCY,
    UPDATE_RENTAL_TENANT,
)
from api.schemas.rental.dictionaries.payload import (
    RentalApartmentCostUpdatePayload,
    RentalApartmentUpdatePayload,
    RentalCostTypeUpdatePayload,
    RentalMeterUpdatePayload,
    RentalTenancyUpdatePayload,
    RentalTenantUpdatePayload,
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
from config.rate_limit import RATE_LIMIT_WRITE, auth_or_ip_key, limiter
from core.data.user import UserData
from core.handler.rental.dictionaries.update import (
    handler_update_apartment,
    handler_update_apartment_cost,
    handler_update_cost_type,
    handler_update_meter,
    handler_update_tenancy,
    handler_update_tenant,
)
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from database.psql.database import get_db

router = APIRouter()

_UPDATE_RESPONSES = {
    400: {"model": ApiErrorResponse, "description": "Niepoprawny format identyfikatora"},
    401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
    403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
    404: {"model": ApiErrorResponse, "description": "Rekord nie istnieje"},
    409: {"model": ApiErrorResponse, "description": "Konflikt danych (IntegrityError)"},
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


@router.put(
    UPDATE_RENTAL_APARTMENT,
    summary="[Superadmin] Zaktualizuj mieszkanie",
    response_model=ApiResponse[RentalApartmentResponseData],
    responses=_UPDATE_RESPONSES,
    status_code=200,
    tags=["Rentals/Dictionaries"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_superadmin_update_rental_apartment(
    request: Request,
    apartment_id: str,
    body: RentalApartmentUpdatePayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[RentalApartmentResponseData] | JSONResponse:
    try:
        if not is_valid_uuid(apartment_id):
            return _invalid_uuid_response("Apartment_id", "api_superadmin_update_rental_apartment")

        data, error, success = handler_update_apartment(
            user_data["id"], apartment_id, body.name, body.description, body.is_active, db_session=db
        )
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=200, data=RentalApartmentResponseData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_update_rental_apartment",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())


@router.put(
    UPDATE_RENTAL_TENANT,
    summary="[Superadmin] Zaktualizuj najemcę",
    response_model=ApiResponse[RentalTenantResponseData],
    responses=_UPDATE_RESPONSES,
    status_code=200,
    tags=["Rentals/Dictionaries"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_superadmin_update_rental_tenant(
    request: Request,
    tenant_id: str,
    body: RentalTenantUpdatePayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[RentalTenantResponseData] | JSONResponse:
    try:
        if not is_valid_uuid(tenant_id):
            return _invalid_uuid_response("Tenant_id", "api_superadmin_update_rental_tenant")

        data, error, success = handler_update_tenant(
            user_data["id"], tenant_id, body.first_name, body.last_name, body.note, body.is_active, db_session=db
        )
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=200, data=RentalTenantResponseData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_update_rental_tenant",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())


@router.put(
    UPDATE_RENTAL_TENANCY,
    summary="[Superadmin] Zaktualizuj najem (czynsz, osoby, daty)",
    response_model=ApiResponse[RentalTenancyResponseData],
    responses=_UPDATE_RESPONSES,
    status_code=200,
    tags=["Rentals/Dictionaries"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_superadmin_update_rental_tenancy(
    request: Request,
    tenancy_id: str,
    body: RentalTenancyUpdatePayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[RentalTenancyResponseData] | JSONResponse:
    try:
        if not is_valid_uuid(tenancy_id):
            return _invalid_uuid_response("Tenancy_id", "api_superadmin_update_rental_tenancy")

        data, error, success = handler_update_tenancy(
            user_data["id"],
            tenancy_id,
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

        return ApiResponse(status="SUCCESS", status_code=200, data=RentalTenancyResponseData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_update_rental_tenancy",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())


@router.put(
    UPDATE_RENTAL_COST_TYPE,
    summary="[Superadmin] Zaktualizuj rodzaj kosztu",
    response_model=ApiResponse[RentalCostTypeResponseData],
    responses=_UPDATE_RESPONSES,
    status_code=200,
    tags=["Rentals/Dictionaries"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_superadmin_update_rental_cost_type(
    request: Request,
    cost_type_id: str,
    body: RentalCostTypeUpdatePayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[RentalCostTypeResponseData] | JSONResponse:
    try:
        if not is_valid_uuid(cost_type_id):
            return _invalid_uuid_response("Cost_type_id", "api_superadmin_update_rental_cost_type")

        data, error, success = handler_update_cost_type(
            user_data["id"], cost_type_id, body.name, body.charge_type, body.is_active, db_session=db
        )
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=200, data=RentalCostTypeResponseData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_update_rental_cost_type",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())


@router.put(
    UPDATE_RENTAL_APARTMENT_COST,
    summary="[Superadmin] Zaktualizuj koszt mieszkania",
    response_model=ApiResponse[RentalApartmentCostResponseData],
    responses=_UPDATE_RESPONSES,
    status_code=200,
    tags=["Rentals/Dictionaries"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_superadmin_update_rental_apartment_cost(
    request: Request,
    apartment_cost_id: str,
    body: RentalApartmentCostUpdatePayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[RentalApartmentCostResponseData] | JSONResponse:
    try:
        if not is_valid_uuid(apartment_cost_id):
            return _invalid_uuid_response("Apartment_cost_id", "api_superadmin_update_rental_apartment_cost")

        data, error, success = handler_update_apartment_cost(
            user_data["id"], apartment_cost_id, body.amount, body.start_date, body.end_date, db_session=db
        )
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=200, data=RentalApartmentCostResponseData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_update_rental_apartment_cost",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())


@router.put(
    UPDATE_RENTAL_METER,
    summary="[Superadmin] Zaktualizuj licznik",
    response_model=ApiResponse[RentalMeterResponseData],
    responses=_UPDATE_RESPONSES,
    status_code=200,
    tags=["Rentals/Dictionaries"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_superadmin_update_rental_meter(
    request: Request,
    meter_id: str,
    body: RentalMeterUpdatePayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[RentalMeterResponseData] | JSONResponse:
    try:
        if not is_valid_uuid(meter_id):
            return _invalid_uuid_response("Meter_id", "api_superadmin_update_rental_meter")

        data, error, success = handler_update_meter(
            user_data["id"], meter_id, body.is_master, body.name, body.is_active, db_session=db
        )
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=200, data=RentalMeterResponseData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_update_rental_meter",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())
