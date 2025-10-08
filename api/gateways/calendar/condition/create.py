from fastapi import Request
from typing import Optional, cast
from api.gateways.types.calendar.condition.create import ApplicationGatewayCalendarConditionCreateResult
from api.calendar.condition.schema import PayloadCalendarConditionCreate
from core.data.response import Error
from core.data.user import UserData

from core.helper.headers import check_required_headers


def application_gateway_calendar_condition_create(
        request: Request,
        payload: PayloadCalendarConditionCreate
) -> tuple[Optional[ApplicationGatewayCalendarConditionCreateResult], Optional[Error], bool, int]:
    try:
        required_headers = ["UserData"]
        data_header = check_required_headers(request, required_headers)
        if not data_header['is_valid']:
            return None, Error(message=data_header['data']['message']), False, data_header['status_code']

        user_data = cast(UserData, data_header['data'][0]['data'])

        if payload.norm_hours is None or not isinstance(payload.norm_hours, (int, float)):
            return None, Error(message="Pole 'norm_hours' musi być liczbą."), False, 422

        if payload.norm_hours <= 0:
            return None, Error(message="Pole 'norm_hours' musi być większe od zera."), False, 422

        if payload.hourly_rate is None or not isinstance(payload.hourly_rate, (int, float)):
            return None, Error(message="Pole 'hourly_rate' musi być liczbą."), False, 422

        if payload.hourly_rate <= 0:
            return None, Error(message="Pole 'hourly_rate' musi być większe od zera."), False, 422

        result: ApplicationGatewayCalendarConditionCreateResult = {
            "norm_hours": float(payload.norm_hours),
            "hourly_rate": float(payload.hourly_rate),
            "user_data": user_data
        }
        return result, None, True, 200

    except Exception as e:
        return None, Error(message=str(e)), False, 417
