from dataclasses import asdict

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, ApiResponse
from api.routers import ADD_ITEM_OUTSTANDING_MONEY, CREATE_LIST_OUTSTANDING_MONEY
from api.schemas.outstanding_money.payload import AddItemPayload, CreateListPayload
from api.schemas.outstanding_money.response import CreatedListData, OutstandingItemData
from config.rate_limit import RATE_LIMIT_WRITE, auth_or_ip_key, limiter
from core.data.user import UserData
from core.handler.outstanding_money.create import handler_add_item, handler_create_list
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from database.psql.database import get_db

router = APIRouter()


@router.post(
    CREATE_LIST_OUTSTANDING_MONEY,
    summary="[Superadmin] Utwórz listę zaległych płatności",
    response_model=ApiResponse[CreatedListData],
    responses={
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        409: {"model": ApiErrorResponse, "description": "Konflikt danych (IntegrityError)"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=201,
    tags=["OutstandingMoney"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_superadmin_create_outstanding_list(
    request: Request,
    body: CreateListPayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[CreatedListData] | JSONResponse:
    try:
        items = [item.model_dump() for item in body.array_object]
        data, error, success = handler_create_list(user_data["id"], body.name, items, db_session=db)
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=201, data=CreatedListData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_create_outstanding_list",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())


@router.post(
    ADD_ITEM_OUTSTANDING_MONEY,
    summary="[Superadmin] Dodaj pozycję do listy zaległości",
    response_model=ApiResponse[OutstandingItemData],
    responses={
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        404: {"model": ApiErrorResponse, "description": "Lista o podanym id_name nie istnieje"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=201,
    tags=["OutstandingMoney"],
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)
def api_superadmin_add_outstanding_item(
    request: Request,
    body: AddItemPayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[OutstandingItemData] | JSONResponse:
    try:
        data, error, success = handler_add_item(user_data["id"], body.id_name, body.amount, body.name, db_session=db)
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=201, data=OutstandingItemData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_add_outstanding_item",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())
