from fastapi import APIRouter, Request, Depends
from api.routers import COLLECTION_OUTSTANDING_MONEY
from consumer.data.response import ResponseApiData
from consumer.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from consumer.handler.outstanding_moeny.collection import handler_collection_list

router = APIRouter()


@router.get(COLLECTION_OUTSTANDING_MONEY, dependencies=[Depends(JWTBasicAuthenticationMiddleware())])
def collection_list(request: Request):
    response = handler_collection_list()
    if not response['is_valid']:
        return ResponseApiData(
            status=response['status'],
            data=response['data'],
            status_code=response['status_code'],
            additional=response['additional']
        ).to_response()

    return ResponseApiData(
        status=response['status'],
        data=response['data'],
        status_code=response['status_code'],
        additional=response['additional']
    ).to_response()
