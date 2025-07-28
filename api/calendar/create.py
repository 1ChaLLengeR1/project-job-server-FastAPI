from typing import cast
from fastapi import APIRouter, Request, Depends
from api.routers import CREATE_CALENDAR
from consumer.data.response import ResponseApiData, Error
from consumer.data.user import UserData
from consumer.helper.headers import check_required_headers
from consumer.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from consumer.handler.calendar.create import handler_create_generator_calendar

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
