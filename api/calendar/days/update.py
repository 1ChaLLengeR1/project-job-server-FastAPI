from typing import cast

from fastapi import APIRouter, Depends

from api.calendar.days.schema import (
    PayloadCalendarDaysWorkSalaryUpdate,
    PayloadCalendarDaysWorkUpdate,
    PayloadCalendarDayWorkUpdateById,
)
from api.gateways.calendar.day.update import (
    application_gateway_calendar_day_by_id_update,
    application_gateway_calendar_days_update,
    application_gateway_calendar_days_update_salary,
)
from api.routers import UPDATE_CALENDAR_DAY_WORK_BY_ID, UPDATE_CALENDAR_DAYS, UPDATE_CALENDAR_DAYS_SALARY
from core.data.response import Error, ResponseApiData
from core.handler.calendar.days.update import (
    handler_update_day_calendary_by_id,
    handler_update_days_automatically_for_salary,
    handler_update_days_calendary,
)
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware

router = APIRouter()


@router.patch(
    UPDATE_CALENDAR_DAY_WORK_BY_ID, dependencies=[Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"]))]
)
def view_update_day_calendary_by_id(day_id: str, payload: PayloadCalendarDayWorkUpdateById):
    try:
        raw_data, raw_error, is_valid, status_code = application_gateway_calendar_day_by_id_update(day_id, payload)

        if not is_valid:
            error = cast(Error, raw_error)
            return ResponseApiData(
                status="ERROR", data={"message": error["message"]}, status_code=status_code, additional=None
            ).to_response()

        day_id: str = raw_data.get("day_id")
        norm_hours: float = raw_data.get("norm_hours")
        hours_worked: float = raw_data.get("hours_worked")
        hourly_rate: float = raw_data.get("hourly_rate")

        response = handler_update_day_calendary_by_id(day_id, norm_hours, hours_worked, hourly_rate)
        return ResponseApiData(
            status=response["status"],
            data=response["data"],
            status_code=response["status_code"],
            additional=response["additional"],
        ).to_response()

    except Exception as e:
        return ResponseApiData(
            status="ERROR", data={"message": f"api_error: {str(e)}"}, status_code=500, additional=None
        ).to_response()


@router.patch(UPDATE_CALENDAR_DAYS, dependencies=[Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"]))])
def view_update_days_calendary(payload: PayloadCalendarDaysWorkUpdate):
    try:
        raw_data, raw_error, is_valid, status_code = application_gateway_calendar_days_update(payload)
        if not is_valid:
            error = cast(Error, raw_error)
            return ResponseApiData(
                status="ERROR", data={"message": error["message"]}, status_code=status_code, additional=None
            ).to_response()

        year: int = raw_data.get("year")
        month: int = raw_data.get("month")
        start_day: int = raw_data.get("start_day")
        end_day: int = raw_data.get("end_day")
        norm_hours: float = raw_data.get("norm_hours")
        hours_worked: float = raw_data.get("hours_worked")
        hourly_rate: float = raw_data.get("hourly_rate")

        response = handler_update_days_calendary(
            year, month, start_day, end_day, norm_hours, hours_worked, hourly_rate
        )
        return ResponseApiData(
            status=response["status"],
            data=response["data"],
            status_code=response["status_code"],
            additional=response["additional"],
        ).to_response()

    except Exception as e:
        return ResponseApiData(
            status="ERROR", data={"message": f"api_error: {str(e)}"}, status_code=500, additional=None
        ).to_response()


@router.patch(
    UPDATE_CALENDAR_DAYS_SALARY, dependencies=[Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"]))]
)
def view_update_days_automatically_for_salary(payload: PayloadCalendarDaysWorkSalaryUpdate):
    try:
        raw_data, raw_error, is_valid, status_code = application_gateway_calendar_days_update_salary(payload)
        if not is_valid:
            error = cast(Error, raw_error)
            return ResponseApiData(
                status="ERROR", data={"message": error["message"]}, status_code=status_code, additional=None
            ).to_response()

        year: int = raw_data.get("year")
        month: int = raw_data.get("month")
        salary: float = raw_data.get("salary")

        response = handler_update_days_automatically_for_salary(year, month, salary)
        return ResponseApiData(
            status=response["status"],
            data=response["data"],
            status_code=response["status_code"],
            additional=response["additional"],
        ).to_response()

    except Exception as e:
        return ResponseApiData(
            status="ERROR", data={"message": f"api_error: {str(e)}"}, status_code=500, additional=None
        ).to_response()
