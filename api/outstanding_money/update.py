from fastapi import APIRouter, Depends

from api.routers import EDIT_ITEM_OUTSTANDING_MONEY, EDIT_NAME_LIST_OUTSTANDING_MONEY
from core.data.response import ResponseApiData
from core.handler.outstanding_moeny.update import handler_edit_item, handler_edit_name_list
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware

from .schemas import EditItem, EditListParams

router = APIRouter()


@router.put(
    EDIT_NAME_LIST_OUTSTANDING_MONEY, dependencies=[Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"]))]
)
def edit_name_list(payload: EditListParams):
    data = {"id": payload.id, "name": payload.name}

    response = handler_edit_name_list(data)
    if not response["is_valid"]:
        return ResponseApiData(
            status=response["status"],
            data=response["data"],
            status_code=response["status_code"],
            additional=response["additional"],
        ).to_response()

    return ResponseApiData(
        status=response["status"],
        data=response["data"],
        status_code=response["status_code"],
        additional=response["additional"],
    ).to_response()


@router.put(
    EDIT_ITEM_OUTSTANDING_MONEY, dependencies=[Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"]))]
)
def edit_item(payload: EditItem):
    data = {"id": payload.id, "amount": payload.amount, "name": payload.name}

    response = handler_edit_item(data)
    if not response["is_valid"]:
        return ResponseApiData(
            status=response["status"],
            data=response["data"],
            status_code=response["status_code"],
            additional=response["additional"],
        ).to_response()

    return ResponseApiData(
        status=response["status"],
        data=response["data"],
        status_code=response["status_code"],
        additional=response["additional"],
    ).to_response()
