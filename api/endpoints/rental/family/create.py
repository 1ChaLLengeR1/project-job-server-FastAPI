from dataclasses import asdict

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, ApiResponse
from api.routers import CREATE_RENTAL_ALLOCATION_RULE, CREATE_RENTAL_BENEFICIARY
from api.schemas.rental.family.payload import (
    RentalAllocationRuleCreatePayload,
    RentalBeneficiaryCreatePayload,
)
from api.schemas.rental.family.response import (
    RentalAllocationRuleResponseData,
    RentalBeneficiaryResponseData,
)
from config.rate_limit import RATE_LIMIT_WRITE, auth_or_ip_key, limiter
from core.data.user import UserData
from core.handler.rental.family.create import (
    handler_create_allocation_rule,
    handler_create_beneficiary,
)
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from database.psql.database import get_db

router = APIRouter()


@router.post(
    CREATE_RENTAL_BENEFICIARY,
    summary="[Superadmin] Utwórz beneficjenta",
    response_model=ApiResponse[RentalBeneficiaryResponseData],
    responses={
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        409: {"model": ApiErrorResponse, "description": "Konflikt danych (IntegrityError)"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=201,
    tags=["Rentals/Family"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_superadmin_create_rental_beneficiary(
    request: Request,
    body: RentalBeneficiaryCreatePayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[RentalBeneficiaryResponseData] | JSONResponse:
    try:
        data, error, success = handler_create_beneficiary(user_data["id"], body.name, body.is_active, db_session=db)
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=201, data=RentalBeneficiaryResponseData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_create_rental_beneficiary",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())


@router.post(
    CREATE_RENTAL_ALLOCATION_RULE,
    summary="[Superadmin] Utwórz regułę podziału rodzinnego",
    response_model=ApiResponse[RentalAllocationRuleResponseData],
    responses={
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        404: {"model": ApiErrorResponse, "description": "Beneficjent, mieszkanie lub rodzaj kosztu nie istnieje"},
        409: {"model": ApiErrorResponse, "description": "Konflikt danych (IntegrityError)"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=201,
    tags=["Rentals/Family"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_superadmin_create_rental_allocation_rule(
    request: Request,
    body: RentalAllocationRuleCreatePayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[RentalAllocationRuleResponseData] | JSONResponse:
    try:
        data, error, success = handler_create_allocation_rule(
            user_data["id"],
            body.beneficiary_id,
            body.component,
            body.mode,
            body.start_date,
            apartment_id=body.apartment_id,
            cost_type_id=body.cost_type_id,
            amount=body.amount,
            description=body.description,
            end_date=body.end_date,
            db_session=db,
        )
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=201, data=RentalAllocationRuleResponseData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_create_rental_allocation_rule",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())
