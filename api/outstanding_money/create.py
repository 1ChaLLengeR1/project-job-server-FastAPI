from fastapi import APIRouter, Depends

from api.routers import ADD_ITEM_OUTSTANDING_MONEY, CREATE_LIST_OUTSTANDING_MONEY
from core.data.response import ResponseApiData
from core.handler.outstanding_moeny.create import handler_add_item, handler_create_list
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware

from .schemas import AddItemParams, KeysCalculatorData

router = APIRouter()


@router.post(
    CREATE_LIST_OUTSTANDING_MONEY, dependencies=[Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"]))]
)
def create_list(payload: KeysCalculatorData):
    data = {"name": payload.name, "array_object": payload.array_object}

    response = handler_create_list(data)
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


@router.post(
    ADD_ITEM_OUTSTANDING_MONEY, dependencies=[Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"]))]
)
def add_item(payload: AddItemParams):
    data = {"id_name": payload.id_name, "amount": payload.amount, "name": payload.name}

    response = handler_add_item(data)
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
