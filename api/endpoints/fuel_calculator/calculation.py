from dataclasses import asdict

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, ApiResponse
from api.routers import FUEL_CALCULATION
from api.schemas.fuel_calculator.payload import FuelCalculationPayload
from api.schemas.fuel_calculator.response import FuelCalculationResponseData
from config.rate_limit import RATE_LIMIT_WRITE, auth_or_ip_key, limiter
from core.data.user import UserData
from core.handler.fuel_calculator.calculation import handler_fuel_calculation
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from database.psql.database import get_db

router = APIRouter()


@router.post(
    FUEL_CALCULATION,
    summary="[User] Oblicz koszt paliwa",
    response_model=ApiResponse[FuelCalculationResponseData],
    responses={
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["FuelCalculator"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_user_fuel_calculation(
    request: Request,
    body: FuelCalculationPayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware()),
    db: Session = Depends(get_db),
) -> ApiResponse[FuelCalculationResponseData] | JSONResponse:
    try:
        data, error, success = handler_fuel_calculation(
            user_data["id"], body.way, body.fuel, body.combustion, body.remaining_values, db_session=db
        )
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=200, data=FuelCalculationResponseData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_user_fuel_calculation",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())
