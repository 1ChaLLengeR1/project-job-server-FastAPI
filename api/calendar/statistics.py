from typing import cast
from fastapi import APIRouter, Request, Depends
from api.gateways.calendar.statistics import application_gateway_calendar_statistics
from api.routers import STATISTICS_CALENDAR
from core.data.response import ResponseApiData, Error
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from core.handler.calendar.statistics import handler_statistics_calendar

router = APIRouter()


@router.get(STATISTICS_CALENDAR, dependencies=[Depends(JWTBasicAuthenticationMiddleware())])
def view_statistics_calendar(request: Request):
    try:
        raw_data, raw_error, is_valid, status_code = application_gateway_calendar_statistics(
            request,
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

        year = raw_data.get("year")

        response = handler_statistics_calendar(year)
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
