from dataclasses import asdict

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, ApiResponse
from api.routers import STATISTICS_CALENDAR
from api.schemas.calendar.response import CalendarStatisticsData
from core.data.user import UserData
from core.handler.calendar.statistics import handler_statistics_calendar
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from database.psql.database import get_db

router = APIRouter()


@router.get(
    STATISTICS_CALENDAR,
    summary="[User] Roczne statystyki kalendarza pracy",
    response_model=ApiResponse[CalendarStatisticsData],
    responses={
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["Calendar"],
)
def api_user_statistics_calendar(
    year: int = Query(ge=2000, le=2100, description="Rok"),
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware()),
    db: Session = Depends(get_db),
) -> ApiResponse[CalendarStatisticsData] | JSONResponse:
    try:
        data, error, success = handler_statistics_calendar(user_data["id"], year, db_session=db)
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=200, data=CalendarStatisticsData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_user_statistics_calendar",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())
