from dataclasses import asdict

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, ApiResponse
from api.routers import FUEL_CALCULATION
from api.schemas.fuel_calculator.payload import FuelCalculationPayload
from api.schemas.fuel_calculator.response import FuelCalculationResponseData
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from core.service.fuel_calculator.calculation import calculation_fuel

router = APIRouter()


@router.post(
    FUEL_CALCULATION,
    summary="[User] Oblicz koszt paliwa",
    response_model=ApiResponse[FuelCalculationResponseData],
    responses={
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["FuelCalculator"],
    dependencies=[Depends(JWTBasicAuthenticationMiddleware())],
)
def api_user_fuel_calculation(
    body: FuelCalculationPayload,
) -> ApiResponse[FuelCalculationResponseData] | JSONResponse:
    try:
        data, error, success = calculation_fuel(body.way, body.fuel, body.combustion, body.remaining_values)
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
