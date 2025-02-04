from fastapi import APIRouter, Request, Depends
from api.routers import CREATE_LOG
from consumer.data.response import ResponseApiData
from consumer.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from consumer.handler.logs.create import handler_create_logs
from consumer.helper.headers import check_required_headers

router = APIRouter()


@router.post(CREATE_LOG, dependencies=[Depends(JWTBasicAuthenticationMiddleware())])
def create_logs(request: Request, description: str):
    required_headers = ["UserData"]
    data_header = check_required_headers(request, required_headers)
    if not data_header['is_valid']:
        return ResponseApiData(
            status="ERROR",
            data=data_header['data'],
            status_code=data_header['status_code'],
            additional=None
        ).to_response()

    user_data = data_header['data'][0]['data']

    response = handler_create_logs(user_data, description)
    if not response['is_valid']:
        return ResponseApiData(
            status=response['status'],
            data=response['data'],
            status_code=response['status_code'],
            additional=response['additional']
        ).to_response()

    return ResponseApiData(
        status=response['status'],
        data=response['data'],
        status_code=response['status_code'],
        additional=response['additional']
    ).to_response()
