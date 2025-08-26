from fastapi import APIRouter, Request, Depends
from api.routers import COLLECTION_CALENDAR_CONDITION
from core.data.response import ResponseApiData
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from core.handler.calendar.condition.collection import handler_collection_work_condition_changes

router = APIRouter()


@router.get(COLLECTION_CALENDAR_CONDITION, dependencies=[Depends(JWTBasicAuthenticationMiddleware())])
def collection_work_condition_changes(request: Request):
    response = handler_collection_work_condition_changes()
    return ResponseApiData(
        status=response['status'],
        data=response['data'],
        status_code=response['status_code'],
        additional=response['additional']
    ).to_response()
