from fastapi import APIRouter, Depends, Request

from api.routers import COLLECTION_CALENDAR_CONDITION
from core.data.response import ResponseApiData
from core.handler.calendar.condition.collection import handler_collection_work_condition_changes
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware

router = APIRouter()


@router.get(COLLECTION_CALENDAR_CONDITION, dependencies=[Depends(JWTBasicAuthenticationMiddleware())])
def collection_work_condition_changes(request: Request):
    response = handler_collection_work_condition_changes()
    return ResponseApiData(
        status=response["status"],
        data=response["data"],
        status_code=response["status_code"],
        additional=response["additional"],
    ).to_response()
