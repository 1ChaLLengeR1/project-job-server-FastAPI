from fastapi import APIRouter, Request
from api.routers import LOGIN, AUTOMATICALLY_LOGIN
from consumer.data.response import ResponseApiData
from .schemas import UserDataPayload
from consumer.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from consumer.helper.headers import check_required_headers

router = APIRouter()


@router.post(LOGIN)
async def login(request: Request, payload: UserDataPayload):
    basic_auth = JWTBasicAuthenticationMiddleware()
    is_valid, mess, data = basic_auth.encode_jwt(payload.username, payload.password)

    if not is_valid:
        return ResponseApiData(
            status="ERROR",
            data=mess,
            status_code=400,
            additional=None
        ).to_response()

    return ResponseApiData(
        status="SUCCESS",
        data=data,
        status_code=200,
        additional=None,
    ).to_response()


@router.get(AUTOMATICALLY_LOGIN)
async def automatically_login(request: Request, user_id: str):
    required_headers = ["X-Refresh-Token"]
    data_header = check_required_headers(request, required_headers)
    if not data_header['is_valid']:
        return ResponseApiData(
            status="ERROR",
            data=data_header['data'],
            status_code=data_header['status_code'],
            additional=None
        ).to_response()

    refresh_token_header = data_header['data'][0]['data']

    basic_auth = JWTBasicAuthenticationMiddleware()
    is_valid, mess, data_user = basic_auth.decode_refresh_jwt(refresh_token_header, user_id)

    if not is_valid:
        return ResponseApiData(
            status="ERROR",
            data=mess,
            status_code=400,
            additional=None
        ).to_response()

    return ResponseApiData(
        status="SUCCESS",
        data=data_user,
        status_code=200,
        additional=None
    ).to_response()
