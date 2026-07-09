from dataclasses import asdict

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, ApiResponse
from api.routers import UPDATE_CALENDAR_DAY_WORK_BY_ID, UPDATE_CALENDAR_DAYS, UPDATE_CALENDAR_DAYS_SALARY
from api.schemas.calendar.payload import DaysRangeUpdatePayload, DaysSalaryUpdatePayload, DayUpdateByIdPayload
from api.schemas.calendar.response import SalaryUpdateData, WorkDaysRangeUpdateData, WorkDayUpdateData
from api.validators import is_valid_uuid
from config.rate_limit import RATE_LIMIT_WRITE, auth_or_ip_key, limiter
from core.data.user import UserData
from core.handler.calendar.days.update import (
    handler_update_day_calendary_by_id,
    handler_update_days_automatically_for_salary,
    handler_update_days_calendary,
)
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from database.psql.database import get_db

router = APIRouter()


@router.patch(
    UPDATE_CALENDAR_DAY_WORK_BY_ID,
    summary="[Superadmin] Zaktualizuj pojedynczy dzień pracy",
    response_model=ApiResponse[WorkDayUpdateData],
    responses={
        400: {"model": ApiErrorResponse, "description": "Niepoprawny format day_id"},
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        404: {"model": ApiErrorResponse, "description": "Dzień pracy nie istnieje"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["Calendar/Days"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_superadmin_update_day_by_id(
    request: Request,
    day_id: str,
    body: DayUpdateByIdPayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[WorkDayUpdateData] | JSONResponse:
    try:
        if not is_valid_uuid(day_id):
            error = ApiErrorData(
                message="Day_id nie jest poprawnego formatu uuid.",
                type_module="api_superadmin_update_day_by_id",
                type_error="validation_error",
                key_type_error="Exception",
            )
            return JSONResponse(status_code=400, content=ApiErrorResponse(status_code=400, data=error).model_dump())

        data, error, success = handler_update_day_calendary_by_id(
            user_data["id"], day_id, body.norm_hours, body.hours_worked, body.hourly_rate, db_session=db
        )
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=200, data=WorkDayUpdateData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_update_day_by_id",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())


@router.patch(
    UPDATE_CALENDAR_DAYS,
    summary="[Superadmin] Zaktualizuj zakres dni pracy",
    response_model=ApiResponse[WorkDaysRangeUpdateData],
    responses={
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        404: {"model": ApiErrorResponse, "description": "Brak dni w podanym zakresie"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["Calendar/Days"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_superadmin_update_days_range(
    request: Request,
    body: DaysRangeUpdatePayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[WorkDaysRangeUpdateData] | JSONResponse:
    try:
        data, error, success = handler_update_days_calendary(
            user_data["id"],
            body.year,
            body.month,
            body.start_day,
            body.end_day,
            body.norm_hours,
            body.hours_worked,
            body.hourly_rate,
            db_session=db,
        )
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=200, data=WorkDaysRangeUpdateData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_update_days_range",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())


@router.patch(
    UPDATE_CALENDAR_DAYS_SALARY,
    summary="[Superadmin] Przelicz stawkę godzinową z wypłaty",
    response_model=ApiResponse[SalaryUpdateData],
    responses={
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        404: {"model": ApiErrorResponse, "description": "Brak dni roboczych z godzinami w miesiącu"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["Calendar/Days"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_superadmin_update_days_salary(
    request: Request,
    body: DaysSalaryUpdatePayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[SalaryUpdateData] | JSONResponse:
    try:
        data, error, success = handler_update_days_automatically_for_salary(
            user_data["id"], body.year, body.month, body.salary, db_session=db
        )
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=200, data=SalaryUpdateData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_update_days_salary",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())
