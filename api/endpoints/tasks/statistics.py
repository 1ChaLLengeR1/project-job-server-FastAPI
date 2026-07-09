from dataclasses import asdict
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, ApiResponse
from api.routers import STATISTICS_TASK
from api.schemas.tasks.response import TaskStatisticsResponseData
from core.data.user import UserData
from core.handler.tasks.statistics import handler_get_task_statistics_task
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from database.psql.database import get_db

router = APIRouter()


@router.get(
    STATISTICS_TASK,
    summary="[User] Statystyki wykonanych tasków",
    response_model=ApiResponse[TaskStatisticsResponseData],
    responses={
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["Tasks"],
)
def api_user_task_statistics(
    start_date: datetime | None = Query(None, description="Początek zakresu statystyk (format: yyyy-mm-dd)"),
    end_date: datetime | None = Query(None, description="Koniec zakresu statystyk (format: yyyy-mm-dd)"),
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware()),
    db: Session = Depends(get_db),
) -> ApiResponse[TaskStatisticsResponseData] | JSONResponse:
    try:
        if not start_date:
            start_date = datetime.now(timezone.utc)
        if not end_date:
            end_date = datetime.now(timezone.utc)

        data, error, success = handler_get_task_statistics_task(user_data["id"], start_date, end_date, db_session=db)
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=200, data=TaskStatisticsResponseData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_user_task_statistics",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())
