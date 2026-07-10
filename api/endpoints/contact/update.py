from dataclasses import asdict

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, ApiResponse
from api.routers import UPDATE_CONTACT_MESSAGE_STATUS
from api.schemas.contact.payload import ContactMessageUpdateStatusPayload
from api.schemas.contact.response import ContactMessageResponseData
from api.validators import is_valid_uuid
from config.rate_limit import RATE_LIMIT_WRITE, auth_or_ip_key, limiter
from core.data.user import UserData
from core.handler.contact.update import handler_update_contact_message_status
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from database.psql.database import get_db

router = APIRouter()


@router.put(
    UPDATE_CONTACT_MESSAGE_STATUS,
    summary="[Superadmin] Zmień status obsługi wiadomości",
    response_model=ApiResponse[ContactMessageResponseData],
    responses={
        400: {"model": ApiErrorResponse, "description": "Niepoprawny format message_id"},
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        404: {"model": ApiErrorResponse, "description": "Wiadomość nie istnieje"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["Contact"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_superadmin_update_contact_message_status(
    request: Request,
    message_id: str,
    body: ContactMessageUpdateStatusPayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[ContactMessageResponseData] | JSONResponse:
    try:
        if not is_valid_uuid(message_id):
            error = ApiErrorData(
                message="Message_id nie jest poprawnego formatu uuid.",
                type_module="api_superadmin_update_contact_message_status",
                type_error="validation_error",
                key_type_error="Exception",
            )
            return JSONResponse(status_code=400, content=ApiErrorResponse(status_code=400, data=error).model_dump())

        data, error, success = handler_update_contact_message_status(
            user_data["id"], message_id, body.status, db_session=db
        )
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=200, data=ContactMessageResponseData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_update_contact_message_status",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())
