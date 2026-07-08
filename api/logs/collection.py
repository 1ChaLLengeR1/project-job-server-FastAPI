from fastapi import APIRouter, Depends, Request

from api.routers import COLLECTION_LOGS
from core.data.response import ResponseApiData
from core.handler.logs.collection import handler_collection_logs
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware

router = APIRouter()


@router.get(COLLECTION_LOGS, dependencies=[Depends(JWTBasicAuthenticationMiddleware())])
def collection_logs(request: Request, number: int):
    response = handler_collection_logs(number)
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
