from dataclasses import asdict
from datetime import date

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, ApiResponse
from api.routers import (
    COLLECTION_RENTAL_ALLOCATION_RULES,
    COLLECTION_RENTAL_BENEFICIARIES,
    COLLECTION_RENTAL_BENEFICIARY_SETTLEMENTS,
)
from api.schemas.rental.family.response import (
    RentalAllocationRuleResponseData,
    RentalBeneficiaryResponseData,
    RentalBeneficiarySettlementResponseData,
)
from api.validators import is_valid_uuid
from config.rate_limit import RATE_LIMIT_READ, auth_or_ip_key, limiter
from core.data.user import UserData
from core.handler.rental.family.collection import (
    handler_collection_allocation_rules,
    handler_collection_beneficiaries,
    handler_collection_beneficiary_settlements,
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
    COLLECTION_RENTAL_BENEFICIARIES,
    summary="[Superadmin] Pobierz listę beneficjentów",
    response_model=ApiResponse[list[RentalBeneficiaryResponseData]],
    responses={
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["Rentals/Family"],
)
@limiter.limit(RATE_LIMIT_READ, key_func=auth_or_ip_key)
def api_superadmin_collection_rental_beneficiaries(
    request: Request,
    is_active: bool | None = Query(default=None, description="Filtr aktywności (None = wszystkie)"),
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[list[RentalBeneficiaryResponseData]] | JSONResponse:
    try:
        data, error, success = handler_collection_beneficiaries(user_data["id"], is_active, db_session=db)
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(
            status="SUCCESS", status_code=200, data=[RentalBeneficiaryResponseData(**asdict(item)) for item in data]
        )
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_collection_rental_beneficiaries",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())


@router.get(
    COLLECTION_RENTAL_ALLOCATION_RULES,
    summary="[Superadmin] Pobierz listę reguł podziału (z historią)",
    response_model=ApiResponse[list[RentalAllocationRuleResponseData]],
    responses={
        400: {"model": ApiErrorResponse, "description": "Niepoprawny format beneficiary_id lub apartment_id"},
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["Rentals/Family"],
)
@limiter.limit(RATE_LIMIT_READ, key_func=auth_or_ip_key)
def api_superadmin_collection_rental_allocation_rules(
    request: Request,
    beneficiary_id: str | None = Query(default=None, description="Filtr po beneficjencie (UUID)"),
    apartment_id: str | None = Query(default=None, description="Filtr po mieszkaniu (UUID)"),
    active_on: date | None = Query(default=None, description="Tylko reguły obowiązujące w danym dniu"),
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[list[RentalAllocationRuleResponseData]] | JSONResponse:
    try:
        if beneficiary_id is not None and not is_valid_uuid(beneficiary_id):
            return _invalid_uuid_response("Beneficiary_id", "api_superadmin_collection_rental_allocation_rules")
        if apartment_id is not None and not is_valid_uuid(apartment_id):
            return _invalid_uuid_response("Apartment_id", "api_superadmin_collection_rental_allocation_rules")

        data, error, success = handler_collection_allocation_rules(
            user_data["id"], beneficiary_id, apartment_id, active_on, db_session=db
        )
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(
            status="SUCCESS", status_code=200, data=[RentalAllocationRuleResponseData(**asdict(item)) for item in data]
        )
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_collection_rental_allocation_rules",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())


@router.get(
    COLLECTION_RENTAL_BENEFICIARY_SETTLEMENTS,
    summary="[Superadmin] Pobierz snapshoty podziału rodzinnego",
    description="Wyniki podziału zapisane przy zamknięciu okresów - filtrowanie po okresie i/lub beneficjencie.",
    response_model=ApiResponse[list[RentalBeneficiarySettlementResponseData]],
    responses={
        400: {"model": ApiErrorResponse, "description": "Niepoprawny format period_id lub beneficiary_id"},
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["Rentals/Family"],
)
@limiter.limit(RATE_LIMIT_READ, key_func=auth_or_ip_key)
def api_superadmin_collection_rental_beneficiary_settlements(
    request: Request,
    period_id: str | None = Query(default=None, description="Filtr po okresie (UUID)"),
    beneficiary_id: str | None = Query(default=None, description="Filtr po beneficjencie (UUID)"),
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[list[RentalBeneficiarySettlementResponseData]] | JSONResponse:
    try:
        if period_id is not None and not is_valid_uuid(period_id):
            return _invalid_uuid_response("Period_id", "api_superadmin_collection_rental_beneficiary_settlements")
        if beneficiary_id is not None and not is_valid_uuid(beneficiary_id):
            return _invalid_uuid_response("Beneficiary_id", "api_superadmin_collection_rental_beneficiary_settlements")

        data, error, success = handler_collection_beneficiary_settlements(
            user_data["id"], period_id, beneficiary_id, db_session=db
        )
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(
            status="SUCCESS",
            status_code=200,
            data=[RentalBeneficiarySettlementResponseData(**asdict(item)) for item in data],
        )
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_collection_rental_beneficiary_settlements",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())
