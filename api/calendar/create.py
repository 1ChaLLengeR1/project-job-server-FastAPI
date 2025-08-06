from typing import cast
from fastapi import APIRouter, Request, Depends
from api.routers import CREATE_CALENDAR
from core.data.response import ResponseApiData
from core.data.user import UserData
from core.helper.headers import check_required_headers
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from core.handler.calendar.days.create import handler_create_generator_calendar

router = APIRouter()


@router.post(CREATE_CALENDAR, dependencies=[Depends(JWTBasicAuthenticationMiddleware())])
def view_create_generator_calendar(request: Request):
    required_headers = ["UserData"]
    data_header = check_required_headers(request, required_headers)
    if not data_header['is_valid']:
        return ResponseApiData(
            status=data_header['status'],
            data=data_header['data'],
            status_code=data_header['status_code'],
            additional=data_header['additional']
        ).to_response()

    user_data = cast(UserData, data_header['data'][0]['data'])

    response = handler_create_generator_calendar(user_data)
    return ResponseApiData(
        status=response['status'],
        data=response['data'],
        status_code=response['status_code'],
        additional=response['additional']
    ).to_response()
