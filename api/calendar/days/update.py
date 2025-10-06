from typing import cast
from fastapi import APIRouter, Request, Depends
from api.calendar.days.schema import PayloadCalendarDayWorkUpdateById, PayloadCalendarDaysWorkUpdate, \
    PayloadCalendarDaysWorkSalaryUpdate
from api.gateways.calendar.day.update import application_gateway_calendar_day_by_id_update, \
    application_gateway_calendar_days_update, application_gateway_calendar_days_update_salary
from api.routers import UPDATE_CALENDAR_DAY_WORK_BY_ID, UPDATE_CALENDAR_DAYS, UPDATE_CALENDAR_DAYS_SALARY
from core.data.response import ResponseApiData, Error
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from core.handler.calendar.days.update import handler_update_days_calendary, handler_update_day_calendary_by_id, handler_update_days_automatically_for_salary

router = APIRouter()


@router.patch(UPDATE_CALENDAR_DAY_WORK_BY_ID, dependencies=[Depends(JWTBasicAuthenticationMiddleware())])
def view_update_day_calendary_by_id(request: Request, day_id: str, payload: PayloadCalendarDayWorkUpdateById):
    try:
        raw_data, raw_error, is_valid, status_code = application_gateway_calendar_day_by_id_update(
            request, day_id, payload
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
        day_id: str = raw_data.get("day_id")
        norm_hours: float = raw_data.get("norm_hours")
        hours_worked: float = raw_data.get("hours_worked")
        hourly_rate: float = raw_data.get("hourly_rate")

        response = handler_update_day_calendary_by_id(
            user_data, day_id, norm_hours, hours_worked, hourly_rate
        )
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
                "message": f"api_error: {str(e)}"
            },
            status_code=500,
            additional=None
        ).to_response()


@router.patch(UPDATE_CALENDAR_DAYS, dependencies=[Depends(JWTBasicAuthenticationMiddleware())])
def view_update_days_calendary(request: Request, payload: PayloadCalendarDaysWorkUpdate):
    try:
        raw_data, raw_error, is_valid, status_code = application_gateway_calendar_days_update(
            request, payload
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
        year: int = raw_data.get("year")
        month: int = raw_data.get("month")
        start_day: int = raw_data.get("start_day")
        end_day: int = raw_data.get("end_day")
        norm_hours: float = raw_data.get("norm_hours")
        hours_worked: float = raw_data.get("hours_worked")
        hourly_rate: float = raw_data.get("hourly_rate")

        response = handler_update_days_calendary(
            user_data, year, month, start_day, end_day, norm_hours, hours_worked, hourly_rate
        )
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
                "message": f"api_error: {str(e)}"
            },
            status_code=500,
            additional=None
        ).to_response()


@router.patch(UPDATE_CALENDAR_DAYS_SALARY, dependencies=[Depends(JWTBasicAuthenticationMiddleware())])
def view_update_days_automatically_for_salary(request: Request, payload: PayloadCalendarDaysWorkSalaryUpdate):
    try:
        raw_data, raw_error, is_valid, status_code = application_gateway_calendar_days_update_salary(
            request, payload
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
        year: int = raw_data.get("year")
        month: int = raw_data.get("month")
        salary: float = raw_data.get("salary")

        response = handler_update_days_automatically_for_salary(
            user_data, year, month, salary
        )
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
                "message": f"api_error: {str(e)}"
            },
            status_code=500,
            additional=None
        ).to_response()