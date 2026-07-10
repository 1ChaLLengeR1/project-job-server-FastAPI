from dataclasses import asdict

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, ApiResponse
from api.routers import CREATE_CONTACT_MESSAGE
from api.schemas.contact.payload import ContactMessageCreatePayload
from api.schemas.contact.response import ContactMessageResponseData
from config.rate_limit import RATE_LIMIT_PUBLIC_CONTACT, limiter
from core.handler.contact.create import handler_create_contact_message
from core.middleware.contact_token_authorization import ContactTokenAuthenticationMiddleware
from database.psql.database import get_db

router = APIRouter()


@router.post(
    CREATE_CONTACT_MESSAGE,
    summary="[Public] Wyślij wiadomość kontaktową",
    description="Publiczny endpoint dla frontendów/backendów. Zamiast JWT usera wymaga nagłówka "
    "`X-Contact-Token` — krótkożyciowego tokena HS256 podpisanego wspólnym sekretem "
    "(claim `application` identyfikuje aplikację nadawcy; instrukcja: docs/CONTACT_TOKEN.md). "
    "Restrykcyjny rate limit per IP.",
    response_model=ApiResponse[ContactMessageResponseData],
    responses={
        401: {"model": ApiErrorResponse, "description": "Brak, niepoprawny lub przeterminowany X-Contact-Token"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań (per IP)"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=201,
    tags=["Contact"],
)
@limiter.limit(RATE_LIMIT_PUBLIC_CONTACT)  # klucz: IP (domyślny get_remote_address) - endpoint publiczny
def api_public_create_contact_message(
    request: Request,
    body: ContactMessageCreatePayload,
    application: str = Depends(ContactTokenAuthenticationMiddleware()),
    db: Session = Depends(get_db),
) -> ApiResponse[ContactMessageResponseData] | JSONResponse:
    try:
        data, error, success = handler_create_contact_message(
            application,
            body.first_name,
            body.phone_number,
            body.description,
            last_name=body.last_name,
            email=body.email,
            db_session=db,
        )
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=201, data=ContactMessageResponseData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_public_create_contact_message",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())
