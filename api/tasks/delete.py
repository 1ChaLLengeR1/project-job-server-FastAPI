from typing import cast

from fastapi import APIRouter, Request, Depends, Query
from api.routers import DELETE_TASK
from consumer.data.response import ResponseApiData, Error
from consumer.helper.headers import check_required_headers
from consumer.helper.validators import is_valid_uuid
from consumer.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from consumer.handler.tasks.delete import handler_delete_task
from consumer.data.user import UserData

router = APIRouter()


@router.delete(DELETE_TASK, dependencies=[Depends(JWTBasicAuthenticationMiddleware())])
def delete_task(request: Request, task_id: str):
    required_headers = ["UserData"]
    data_header = check_required_headers(request, required_headers)
    if not data_header['is_valid']:
        return ResponseApiData(
            status="ERROR",
            data=data_header['data'],
            status_code=data_header['status_code'],
            additional=None
        ).to_response()

    user_data = cast(UserData, data_header['data'][0]['data'])

    if not is_valid_uuid(task_id):
        return ResponseApiData(
            status="ERROR",
            data={"message": "Task_id nie jest poprawnego formatu uuid."},
            status_code=400,
            additional=None
        ).to_response()

    response = handler_delete_task(user_data, task_id)
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
