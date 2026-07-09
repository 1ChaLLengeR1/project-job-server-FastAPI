from dataclasses import asdict

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, ApiResponse
from api.routers import CALCULATOR
from api.schemas.patryk_router.payload import CalculationPayload
from api.schemas.patryk_router.response import CalculationResponseData
from core.data.user import UserData
from core.handler.patryk.calculator_work.calculator import handler_calculations
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from database.psql.database import get_db

router = APIRouter()


@router.post(
    CALCULATOR,
    summary="[Admin] Oblicz zysk ze sprzedaży",
    response_model=ApiResponse[CalculationResponseData],
    responses={
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola admin)"},
        404: {"model": ApiErrorResponse, "description": "Brak rekordu kluczy kalkulatora"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["Patryk/Calculator"],
)
def api_admin_calculations(
    body: CalculationPayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["admin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[CalculationResponseData] | JSONResponse:
    try:
        data, error, success = handler_calculations(
            user_data["id"],
            body.gross_sales,
            body.gross_purchase,
            body.provision,
            body.distinction,
            body.referrer,
            db_session=db,
        )
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=200, data=CalculationResponseData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_admin_calculations",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())
