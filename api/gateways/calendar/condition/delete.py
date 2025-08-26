from fastapi import Request
from typing import Optional, cast
from api.gateways.types.calendar.condition.delete import ApplicationGatewayCalendarConditionDeleteResult
from core.data.response import Error
from core.data.user import UserData
from core.helper.validators import is_valid_uuid

from core.helper.headers import check_required_headers


def application_gateway_calendar_condition_delete(
        request: Request,
        condition_id: str
) -> tuple[Optional[ApplicationGatewayCalendarConditionDeleteResult], Optional[Error], bool, int]:
    try:
        required_headers = ["UserData"]
        data_header = check_required_headers(request, required_headers)
        if not data_header['is_valid']:
            return None, Error(message=data_header['data']['message']), False, data_header['status_code']

        user_data = cast(UserData, data_header['data'][0]['data'])

        if not is_valid_uuid(condition_id):
            return None, Error(message="Pole 'condition_id' musi być prawidłowym UUID."), False, 422

        result: ApplicationGatewayCalendarConditionDeleteResult = {
            "condition_id": condition_id,
            "user_data": user_data
        }
        return result, None, True, 200
    except Exception as e:
        return None, Error(message=str(e)), False, 417