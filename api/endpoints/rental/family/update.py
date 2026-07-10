from dataclasses import asdict

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, ApiResponse
from api.routers import UPDATE_RENTAL_ALLOCATION_RULE, UPDATE_RENTAL_BENEFICIARY
from api.schemas.rental.family.payload import (
    RentalAllocationRuleUpdatePayload,
    RentalBeneficiaryUpdatePayload,
)
from api.schemas.rental.family.response import (
    RentalAllocationRuleResponseData,
    RentalBeneficiaryResponseData,
)
from api.validators import is_valid_uuid
from config.rate_limit import RATE_LIMIT_WRITE, auth_or_ip_key, limiter
from core.data.user import UserData
from core.handler.rental.family.update import (
    handler_update_allocation_rule,
    handler_update_beneficiary,
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
    UPDATE_RENTAL_BENEFICIARY,
    summary="[Superadmin] Zaktualizuj beneficjenta",
    response_model=ApiResponse[RentalBeneficiaryResponseData],
    responses=_UPDATE_RESPONSES,
    status_code=200,
    tags=["Rentals/Family"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_superadmin_update_rental_beneficiary(
    request: Request,
    beneficiary_id: str,
    body: RentalBeneficiaryUpdatePayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[RentalBeneficiaryResponseData] | JSONResponse:
    try:
        if not is_valid_uuid(beneficiary_id):
            return _invalid_uuid_response("Beneficiary_id", "api_superadmin_update_rental_beneficiary")

        data, error, success = handler_update_beneficiary(
            user_data["id"], beneficiary_id, body.name, body.is_active, db_session=db
        )
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=200, data=RentalBeneficiaryResponseData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_update_rental_beneficiary",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())


@router.put(
    UPDATE_RENTAL_ALLOCATION_RULE,
    summary="[Superadmin] Zaktualizuj regułę podziału",
    response_model=ApiResponse[RentalAllocationRuleResponseData],
    responses=_UPDATE_RESPONSES,
    status_code=200,
    tags=["Rentals/Family"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_superadmin_update_rental_allocation_rule(
    request: Request,
    rule_id: str,
    body: RentalAllocationRuleUpdatePayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[RentalAllocationRuleResponseData] | JSONResponse:
    try:
        if not is_valid_uuid(rule_id):
            return _invalid_uuid_response("Rule_id", "api_superadmin_update_rental_allocation_rule")

        data, error, success = handler_update_allocation_rule(
            user_data["id"],
            rule_id,
            body.apartment_id,
            body.component,
            body.cost_type_id,
            body.mode,
            body.amount,
            body.description,
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

        return ApiResponse(status="SUCCESS", status_code=200, data=RentalAllocationRuleResponseData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_update_rental_allocation_rule",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())
