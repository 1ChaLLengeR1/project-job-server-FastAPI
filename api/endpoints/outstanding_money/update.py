from dataclasses import asdict

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.response import ERROR_STATUS_CODES, ApiErrorData, ApiErrorResponse, ApiResponse
from api.routers import EDIT_ITEM_OUTSTANDING_MONEY, EDIT_NAME_LIST_OUTSTANDING_MONEY
from api.schemas.outstanding_money.payload import EditItemPayload, EditListPayload
from api.schemas.outstanding_money.response import NamesOverdueData, OutstandingItemData
from core.data.user import UserData
from core.handler.outstanding_money.update import handler_edit_item, handler_edit_name_list
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from database.psql.database import get_db

router = APIRouter()


@router.put(
    EDIT_NAME_LIST_OUTSTANDING_MONEY,
    summary="[Superadmin] Zmień nazwę listy zaległości",
    response_model=ApiResponse[NamesOverdueData],
    responses={
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        404: {"model": ApiErrorResponse, "description": "Lista o podanym id nie istnieje"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["OutstandingMoney"],
)
def api_superadmin_edit_outstanding_list_name(
    body: EditListPayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[NamesOverdueData] | JSONResponse:
    try:
        data, error, success = handler_edit_name_list(user_data["id"], body.id, body.name, db_session=db)
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=200, data=NamesOverdueData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_edit_outstanding_list_name",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())


@router.put(
    EDIT_ITEM_OUTSTANDING_MONEY,
    summary="[Superadmin] Edytuj pozycję listy zaległości",
    response_model=ApiResponse[OutstandingItemData],
    responses={
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        404: {"model": ApiErrorResponse, "description": "Pozycja o podanym id nie istnieje"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=200,
    tags=["OutstandingMoney"],
)
def api_superadmin_edit_outstanding_item(
    body: EditItemPayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[OutstandingItemData] | JSONResponse:
    try:
        data, error, success = handler_edit_item(user_data["id"], body.id, body.amount, body.name, db_session=db)
        if not success:
            status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
            return JSONResponse(
                status_code=status_code,
                content=ApiErrorResponse(status_code=status_code, data=error).model_dump(),
            )

        return ApiResponse(status="SUCCESS", status_code=200, data=OutstandingItemData(**asdict(data)))
    except Exception as e:
        error = ApiErrorData(
            message=str(e),
            type_module="api_superadmin_edit_outstanding_item",
            type_error="exception",
            key_type_error="Exception",
        )
        return JSONResponse(status_code=500, content=ApiErrorResponse(status_code=500, data=error).model_dump())
