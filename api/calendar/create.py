from typing import cast
from fastapi import APIRouter, Request, Depends
from api.calendar.schema import PayloadCalendarCreate
from api.gateways.calendar.create import application_gateway_calendar_create
from api.routers import CREATE_CALENDAR
from core.data.response import ResponseApiData, Error
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from core.handler.calendar.create import handler_create_generator_calendar

router = APIRouter()


@router.post(CREATE_CALENDAR, dependencies=[Depends(JWTBasicAuthenticationMiddleware())])
def view_create_generator_calendar(request: Request, payload: PayloadCalendarCreate):
    try:
        raw_data, raw_error, is_valid, status_code = application_gateway_calendar_create(
            request,
            payload.year
        )

        if not is_valid:
            error = cast(Error, raw_error)
            return ResponseApiData(
                status="ERROR",
                data={
                    "message": error['message']
                },
                status_code=status_code,
                additional=None
            ).to_response()

        user_data = raw_data.get("user_data")
        year = raw_data.get("year")

        response = handler_create_generator_calendar(user_data, year)
        return ResponseApiData(
            status=response['status'],
            data=response['data'],
            status_code=response['status_code'],
            additional=response['additional']
        ).to_response()
    except Exception as e:
        return ResponseApiData(
            status="ERROR",
            data={
                "message": str(e)
            },
            status_code=500,
            additional=None
        ).to_response()
