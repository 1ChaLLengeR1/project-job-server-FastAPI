from fastapi import Request
from typing import Optional, cast

from api.calendar.days.schema import PayloadCalendarDayWorkUpdateById, PayloadCalendarDaysWorkUpdate, \
    PayloadCalendarDaysWorkSalaryUpdate
from api.gateways.types.calendar.condition.delete import ApplicationGatewayCalendarConditionDeleteResult
from core.data.response import Error
from core.data.user import UserData
from core.helper.validators import is_valid_uuid

from core.helper.headers import check_required_headers


def application_gateway_calendar_day_by_id_update(
        request: Request,
        day_id: str,
        payload: PayloadCalendarDayWorkUpdateById
) -> tuple[Optional[dict], Optional[Error], bool, int]:
    try:
        required_headers = ["UserData"]
        data_header = check_required_headers(request, required_headers)
        if not data_header['is_valid']:
            return None, Error(message=data_header['data']['message']), False, data_header['status_code']

        user_data = cast(UserData, data_header['data'][0]['data'])
        user_id: str = user_data['id']

        if not is_valid_uuid(user_id):
            return None, Error(message="Pole 'user_id' musi być prawidłowym UUID."), False, 422

        if not is_valid_uuid(day_id):
            return None, Error(message="Pole 'day_id' musi być prawidłowym UUID."), False, 422

        if payload.norm_hours < 0:
            return None, Error(message="Pole 'norm_hours' nie może być ujemne."), False, 422

        if payload.norm_hours > 24:
            return None, Error(message="Pole 'norm_hours' nie może przekraczać 24 godzin."), False, 422

        if payload.hours_worked < 0:
            return None, Error(message="Pole 'hours_worked' nie może być ujemne."), False, 422

        if payload.hours_worked > 24:
            return None, Error(message="Pole 'hours_worked' nie może przekraczać 24 godzin."), False, 422

        if payload.hourly_rate < 0:
            return None, Error(message="Pole 'hourly_rate' nie może być ujemne."), False, 422

        return {
            "user_data": user_data,
            "day_id": day_id,
            "norm_hours": payload.norm_hours,
            "hours_worked": payload.hours_worked,
            "hourly_rate": payload.hourly_rate,
        }, None, True, 200

    except Exception as e:
        return None, Error(message=str(e)), False, 400


def application_gateway_calendar_days_update(
        request: Request,
        payload: PayloadCalendarDaysWorkUpdate
) -> tuple[Optional[dict], Optional[Error], bool, int]:
    try:
        required_headers = ["UserData"]
        data_header = check_required_headers(request, required_headers)
        if not data_header['is_valid']:
            return None, Error(message=data_header['data']['message']), False, data_header['status_code']

        user_data = cast(UserData, data_header['data'][0]['data'])
        user_id: str = user_data['id']

        if not is_valid_uuid(user_id):
            return None, Error(message="Pole 'user_id' musi być prawidłowym UUID."), False, 422

        if payload.year < 1900 or payload.year > 2100:
            return None, Error(message="Pole 'year' musi być w zakresie 1900-2100."), False, 422

        if payload.month < 1 or payload.month > 12:
            return None, Error(message="Pole 'month' musi być w zakresie 1-12."), False, 422

        if payload.start_day < 1 or payload.start_day > 31:
            return None, Error(message="Pole 'start_day' musi być w zakresie 1-31."), False, 422

        if payload.end_day < 1 or payload.end_day > 31:
            return None, Error(message="Pole 'end_day' musi być w zakresie 1-31."), False, 422

        if payload.start_day > payload.end_day:
            return None, Error(message="Pole 'start_day' nie może być większe niż 'end_day'."), False, 422

        if payload.norm_hours < 0:
            return None, Error(message="Pole 'norm_hours' nie może być ujemne."), False, 422

        if payload.norm_hours > 24:
            return None, Error(message="Pole 'norm_hours' nie może przekraczać 24 godzin."), False, 422

        if payload.hours_worked < 0:
            return None, Error(message="Pole 'hours_worked' nie może być ujemne."), False, 422

        if payload.hours_worked > 24:
            return None, Error(message="Pole 'hours_worked' nie może przekraczać 24 godzin."), False, 422

        if payload.hourly_rate < 0:
            return None, Error(message="Pole 'hourly_rate' nie może być ujemne."), False, 422

        return {
            "user_data": user_data,
            "year": payload.year,
            "month": payload.month,
            "start_day": payload.start_day,
            "end_day": payload.end_day,
            "norm_hours": payload.norm_hours,
            "hours_worked": payload.hours_worked,
            "hourly_rate": payload.hourly_rate,
        }, None, True, 200

    except Exception as e:
        return None, Error(message=str(e)), False, 400


def application_gateway_calendar_days_update_salary(
        request: Request,
        payload: PayloadCalendarDaysWorkSalaryUpdate
) -> tuple[Optional[dict], Optional[Error], bool, int]:
    try:
        required_headers = ["UserData"]
        data_header = check_required_headers(request, required_headers)
        if not data_header['is_valid']:
            return None, Error(message=data_header['data']['message']), False, data_header['status_code']

        user_data = cast(UserData, data_header['data'][0]['data'])
        user_id: str = user_data['id']

        if not is_valid_uuid(user_id):
            return None, Error(message="Pole 'user_id' musi być prawidłowym UUID."), False, 422

        if payload.year < 1900 or payload.year > 2100:
            return None, Error(message="Pole 'year' musi być w zakresie 1900-2100."), False, 422

        if payload.month < 1 or payload.month > 12:
            return None, Error(message="Pole 'month' musi być w zakresie 1-12."), False, 422

        if payload.salary < 0:
            return None, Error(message="Pole 'salary' musi być być większe od 0"), False, 422

        return {
            "user_data": user_data,
            "year": payload.year,
            "month": payload.month,
            "salary": payload.salary,
        }, None, True, 200

    except Exception as e:
        return None, Error(message=str(e)), False, 400
