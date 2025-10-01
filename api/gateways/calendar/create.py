from fastapi import Request
from typing import Optional, cast
from datetime import datetime
from core.data.response import Error
from core.data.user import UserData

from core.helper.headers import check_required_headers


def application_gateway_calendar_create(
        request: Request,
        year: int
) -> tuple[Optional[dict], Optional[Error], bool, int]:
    try:
        required_headers = ["UserData"]
        data_header = check_required_headers(request, required_headers)
        if not data_header['is_valid']:
            return None, Error(message=data_header['data']['message']), False, data_header['status_code']

        user_data = cast(UserData, data_header['data'][0]['data'])

        current_year = datetime.now().year
        min_year = 2000
        max_year = current_year + 10

        if year < min_year or year > max_year:
            return None, Error(
                message=f"Year must be between {min_year} and {max_year}"
            ), False, 400

        result = {
            "user_data": user_data,
            "year": year,
        }
        return result, None, True, 200

    except Exception as e:
        return None, Error(message=str(e)), False, 417
