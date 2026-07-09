from dataclasses import asdict

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, ApiResponse
from api.routers import CREATE_CALENDAR
from api.schemas.calendar.payload import CalendarCreatePayload
from api.schemas.calendar.response import GeneratedCalendarData
from core.data.user import UserData
from core.handler.calendar.create import handler_create_generator_calendar
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from database.psql.database import get_db

router = APIRouter()


@router.post(
    CREATE_CALENDAR,
    summary="[Superadmin] Wygeneruj kalendarz pracy na rok",
    response_model=ApiResponse[GeneratedCalendarData],
    responses={
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        404: {"model": ApiErrorResponse, "description": "Brak warunków pracy w bazie"},
        409: {"model": ApiErrorResponse, "description": "Kalendarz na ten rok już istnieje"},
        502: {"model": ApiErrorResponse, "description": "Błąd zewnętrznego API świąt (date.nager.at)"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=201,
    tags=["Calendar"],
)
def api_superadmin_create_calendar(
    body: CalendarCreatePayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[GeneratedCalendarData] | JSONResponse:
    try:
        data, error, success = handler_create_generator_calendar(user_data["id"], body.year, db_session=db)
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=201, data=GeneratedCalendarData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_create_calendar",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())
