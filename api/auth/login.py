from fastapi import APIRouter, Header

from api.routers import AUTOMATICALLY_LOGIN, LOGIN
from core.data.response import ResponseApiData
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware

from .schemas import UserDataPayload

router = APIRouter()


@router.post(LOGIN)
def login(payload: UserDataPayload):
    basic_auth = JWTBasicAuthenticationMiddleware()
    is_valid, mess, data = basic_auth.encode_jwt(payload.username, payload.password)

    if not is_valid:
        return ResponseApiData(status="ERROR", data=mess, status_code=400, additional=None).to_response()

    return ResponseApiData(
        status="SUCCESS",
        data=data,
        status_code=200,
        additional=None,
    ).to_response()


@router.get(AUTOMATICALLY_LOGIN)
def automatically_login(user_id: str, x_refresh_token: str = Header(alias="X-Refresh-Token")):
    basic_auth = JWTBasicAuthenticationMiddleware()
    is_valid, mess, data_user = basic_auth.decode_refresh_jwt(x_refresh_token, user_id)

    if not is_valid:
        return ResponseApiData(status="ERROR", data=mess, status_code=400, additional=None).to_response()

    return ResponseApiData(status="SUCCESS", data=data_user, status_code=200, additional=None).to_response()
