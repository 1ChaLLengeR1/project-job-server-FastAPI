from dataclasses import asdict

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, ApiResponse
from api.routers import AUTOMATICALLY_LOGIN, LOGIN
from api.schemas.auth.payload import LoginPayload
from api.schemas.auth.response import AuthTokensData
from core.data.user import UserData
from core.handler.auth.login import handler_automatically_login, handler_login
from core.middleware.refresh_authorization import JWTRefreshAuthenticationMiddleware
from database.psql.database import get_db

router = APIRouter()


@router.post(
    LOGIN,
    summary="[Public] Zaloguj użytkownika",
    response_model=ApiResponse[AuthTokensData],
    responses={
        401: {"model": ApiErrorResponse, "description": "Błędna nazwa użytkownika lub hasło"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["Auth"],
)
def api_public_login(
    body: LoginPayload,
    db: Session = Depends(get_db),
) -> ApiResponse[AuthTokensData] | JSONResponse:
    try:
        data, error, success = handler_login(body.username, body.password, db_session=db)
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=200, data=AuthTokensData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_public_login",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())


@router.get(
    AUTOMATICALLY_LOGIN,
    summary="[Public] Odśwież sesję refresh tokenem",
    response_model=ApiResponse[AuthTokensData],
    responses={
        400: {"model": ApiErrorResponse, "description": "Niepoprawny format user_id"},
        401: {"model": ApiErrorResponse, "description": "Niepoprawny lub cudzy refresh token"},
        404: {"model": ApiErrorResponse, "description": "User nie istnieje"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["Auth"],
)
def api_public_automatically_login(
    user_data: UserData = Depends(JWTRefreshAuthenticationMiddleware()),
    db: Session = Depends(get_db),
) -> ApiResponse[AuthTokensData] | JSONResponse:
    try:
        data, error, success = handler_automatically_login(user_data["id"], user_data["username"], db_session=db)
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=200, data=AuthTokensData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_public_automatically_login",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())
