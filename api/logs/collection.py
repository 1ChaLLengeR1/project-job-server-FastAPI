from fastapi import APIRouter, Request, Depends
from api.routers import COLLECTION_LOGS
from consumer.data.response import ResponseApiData
from consumer.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from consumer.handler.logs.collection import handler_collection_logs
from consumer.helper.headers import check_required_headers

router = APIRouter()


@router.get(COLLECTION_LOGS, dependencies=[Depends(JWTBasicAuthenticationMiddleware())])
def collection_logs(request: Request, number: int):
    response = handler_collection_logs(number)
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
