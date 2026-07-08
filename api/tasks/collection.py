from fastapi import APIRouter, Depends, Query, Request

from api.routers import COLLECTION_TASKS
from core.data.response import ResponseApiData
from core.handler.tasks.collection import handler_collection_task
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware

router = APIRouter()


@router.get(COLLECTION_TASKS, dependencies=[Depends(JWTBasicAuthenticationMiddleware())])
def collection_task(request: Request, active: bool = Query(default=True)):
    response = handler_collection_task(active)
    return ResponseApiData(
        status=response["status"],
        data=response["data"],
        status_code=response["status_code"],
        additional=response["additional"],
    ).to_response()
