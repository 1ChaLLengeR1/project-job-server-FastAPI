from typing import cast
from fastapi import APIRouter, Request, Depends

from api.gateways.calendar.collection import application_gateway_calendar_collection
from api.routers import COLLECTION_CALENDAR
from core.data.response import ResponseApiData, Error
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from core.handler.calendar.collection import handler_collection_calendar

router = APIRouter()


@router.get(COLLECTION_CALENDAR, dependencies=[Depends(JWTBasicAuthenticationMiddleware())])
def view_collection_calendar(request: Request):
    try:
        raw_data, raw_error, is_valid, status_code = application_gateway_calendar_collection(
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
        month = raw_data.get("month")

        response = handler_collection_calendar(year, month)
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
