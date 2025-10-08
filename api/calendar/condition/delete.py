from typing import cast
from fastapi import APIRouter, Request, Depends
from api.routers import DELETE_CALENDAR_CONDITION
from api.gateways.calendar.condition.delete import application_gateway_calendar_condition_delete
from core.data.response import ResponseApiData, Error
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from core.handler.calendar.condition.delete import handler_delete_work_condition_change

router = APIRouter()


@router.delete(DELETE_CALENDAR_CONDITION, dependencies=[Depends(JWTBasicAuthenticationMiddleware())])
def delete_work_condition_change(request: Request, condition_id: str):
    raw_data, raw_error, is_valid, status_code = application_gateway_calendar_condition_delete(request, condition_id)

    if not is_valid:
        error = cast(Error, raw_error)
        return ResponseApiData(
            status="ERROR",
            data={
                "message": error['message']
            },
            status_code=status_code,
            additional=None
        ).to_response()

    response = handler_delete_work_condition_change(
        user_data=raw_data['user_data'],
        condition_id=raw_data['condition_id']
    )
    return ResponseApiData(
        status=response['status'],
        data=response['data'],
        status_code=response['status_code'],
        additional=response['additional']
    ).to_response()