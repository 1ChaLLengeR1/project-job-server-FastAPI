from fastapi import APIRouter, Request
from api.routers import LOGIN, AUTOMATICALLY_LOGIN
from consumer.data.response import ResponseApiData
from .schemas import UserDataPayload
from consumer.middleware.basic_authorization import JWTBasicAuthenticationMiddleware

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
        )

    return ResponseApiData(
        status="SUCCESS",
        data=data,
        status_code=200,
        additional=None,
    )


@router.get(AUTOMATICALLY_LOGIN)
async def automatically_login(request: Request, user_id: str):
    refresh_token_header = request.headers.get("X-Refresh-Token")
    if not refresh_token_header:
        return ResponseApiData(
            status="ERROR",
            data=str("You did not provide authorization headers."),
            status_code=400,
            additional=None
        )

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
