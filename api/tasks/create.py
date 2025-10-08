from fastapi import APIRouter, Request, Depends
from typing import cast
from api.gateways.tasks.create import application_gateway_task_create
from api.gateways.types.tasks.create import ApplicationGatewayTaskCreateResult
from api.routers import CREATE_TASK
from core.data.response import ResponseApiData, Error
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from core.handler.tasks.create import handler_create_task
from api.tasks.schemas import PayloadTaskCreate

router = APIRouter()


@router.post(CREATE_TASK, dependencies=[Depends(JWTBasicAuthenticationMiddleware())])
def create_list(request: Request, payload: PayloadTaskCreate):
    raw_data, raw_error, is_valid, status_code = application_gateway_task_create(request, payload)
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

    data = cast(ApplicationGatewayTaskCreateResult, raw_data)

    response = handler_create_task(data['user_data'], data['description'], data['time'], data['active'])
    return ResponseApiData(
        status=response['status'],
        data=response['data'],
        status_code=response['status_code'],
        additional=response['additional']
    ).to_response()
