from fastapi import APIRouter, Depends, Request

from api.routers import COLLECTION_OUTSTANDING_MONEY
from core.data.response import ResponseApiData
from core.handler.outstanding_moeny.collection import handler_collection_list
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware

router = APIRouter()


@router.get(COLLECTION_OUTSTANDING_MONEY, dependencies=[Depends(JWTBasicAuthenticationMiddleware())])
def collection_list(request: Request):
    response = handler_collection_list()
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
