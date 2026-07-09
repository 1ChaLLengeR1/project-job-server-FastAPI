from typing import cast

from fastapi import APIRouter, Depends

from api.calendar.condition.schema import PayloadCalendarConditionCreate
from api.gateways.calendar.condition.update import application_gateway_calendar_condition_update
from api.routers import UPDATE_CALENDAR_CONDITION
from core.data.response import Error, ResponseApiData
from core.handler.calendar.condition.update import handler_update_work_condition_change
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware

router = APIRouter()


@router.patch(UPDATE_CALENDAR_CONDITION, dependencies=[Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"]))])
def create_work_condition_change(condition_id: str, payload: PayloadCalendarConditionCreate):
    raw_data, raw_error, is_valid, status_code = application_gateway_calendar_condition_update(condition_id, payload)

    if not is_valid:
        error = cast(Error, raw_error)
        return ResponseApiData(
            status="ERROR", data={"message": error["message"]}, status_code=status_code, additional=None
        ).to_response()

    response = handler_update_work_condition_change(
        condition_id=raw_data["condition_id"],
        norm_hours=raw_data["norm_hours"],
        hourly_rate=raw_data["hourly_rate"],
    )
    return ResponseApiData(
        status=response["status"],
        data=response["data"],
        status_code=response["status_code"],
        additional=response["additional"],
    ).to_response()
