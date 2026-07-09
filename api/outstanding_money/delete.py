from fastapi import APIRouter, Depends

from api.routers import DELETE_ITEM_OUTSTANDING_MONEY, DELETE_LIST_OUTSTANDING_MONEY
from core.data.response import ResponseApiData
from core.handler.outstanding_moeny.delete import handler_delete_item, handler_delete_list
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware

router = APIRouter()


@router.delete(
    DELETE_LIST_OUTSTANDING_MONEY, dependencies=[Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"]))]
)
def delete_list(id: str):
    response = handler_delete_list(id)
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


@router.delete(
    DELETE_ITEM_OUTSTANDING_MONEY, dependencies=[Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"]))]
)
def delete_item(id: str):
    response = handler_delete_item(id)
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
