from dataclasses import asdict

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, ApiResponse
from api.routers import DELETE_CALENDAR_CONDITION
from api.schemas.calendar.response import WorkConditionData
from api.validators import is_valid_uuid
from config.rate_limit import RATE_LIMIT_WRITE, auth_or_ip_key, limiter
from core.data.user import UserData
from core.handler.calendar.condition.delete import handler_delete_work_condition_change
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from database.psql.database import get_db

router = APIRouter()


@router.delete(
    DELETE_CALENDAR_CONDITION,
    summary="[Superadmin] Usuń warunki pracy",
    response_model=ApiResponse[WorkConditionData],
    responses={
        400: {"model": ApiErrorResponse, "description": "Niepoprawny format condition_id"},
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        404: {"model": ApiErrorResponse, "description": "Warunki pracy nie istnieją"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["Calendar/Conditions"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_superadmin_delete_work_condition(
    request: Request,
    condition_id: str,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[WorkConditionData] | JSONResponse:
    try:
        if not is_valid_uuid(condition_id):
            error = ApiErrorData(
                message="Condition_id nie jest poprawnego formatu uuid.",
                type_module="api_superadmin_delete_work_condition",
                type_error="validation_error",
                key_type_error="Exception",
            )
            return JSONResponse(status_code=400, content=ApiErrorResponse(status_code=400, data=error).model_dump())

        data, error, success = handler_delete_work_condition_change(user_data["id"], condition_id, db_session=db)
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=200, data=WorkConditionData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_delete_work_condition",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())
