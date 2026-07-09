from typing import cast

from fastapi import APIRouter, Depends

from api.calendar.condition.schema import PayloadCalendarConditionCreate
from api.gateways.calendar.condition.create import application_gateway_calendar_condition_create
from api.routers import CREATE_CALENDAR_CONDITION
from core.data.response import Error, ResponseApiData
from core.handler.calendar.condition.create import handler_create_work_condition_change
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware

router = APIRouter()


@router.post(CREATE_CALENDAR_CONDITION, dependencies=[Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"]))])
def create_work_condition_change(payload: PayloadCalendarConditionCreate):
    raw_data, raw_error, is_valid, status_code = application_gateway_calendar_condition_create(payload)

    if not is_valid:
        error = cast(Error, raw_error)
        return ResponseApiData(
            status="ERROR", data={"message": error["message"]}, status_code=status_code, additional=None
        ).to_response()

    response = handler_create_work_condition_change(
        norm_hours=raw_data["norm_hours"], hourly_rate=raw_data["hourly_rate"]
    )
    return ResponseApiData(
        status=response["status"],
        data=response["data"],
        status_code=response["status_code"],
        additional=response["additional"],
    ).to_response()
