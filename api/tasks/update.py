from typing import cast

from fastapi import APIRouter, Request, Depends, Query
from api.routers import UPDATE_TASKS, UPDATE_ACTIVE_TASKS
from core.data.response import ResponseApiData, Error
from core.helper.headers import check_required_headers
from core.helper.validators import is_valid_uuid
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from core.handler.tasks.update import handler_update_task, handler_update_task_active
from api.tasks.schemas import PayloadTaskUpdate, PayloadTaskUpdateActive
from core.data.user import UserData

router = APIRouter()


@router.patch(UPDATE_TASKS, dependencies=[Depends(JWTBasicAuthenticationMiddleware())])
def update_task(request: Request, payload: PayloadTaskUpdate, task_id: str):
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

    if payload.description is None or payload.description == "":
        return ResponseApiData(
            status="ERROR",
            data={"message": "W body nie ma klucza 'description' lub jest on pustym stringiem lub nullem."},
            status_code=400,
            additional=None
        ).to_response()

    if payload.time is None or not isinstance(payload.time, int):
        return ResponseApiData(
            status="ERROR",
            data={"message": "W body nie ma klucza 'time' lub jest on nullem bądź nie liczbą."},
            status_code=400,
            additional=None
        ).to_response()

    response = handler_update_task(user_data, task_id, payload.description, payload.time)
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


@router.patch(UPDATE_ACTIVE_TASKS, dependencies=[Depends(JWTBasicAuthenticationMiddleware())])
def update_task_active(request: Request, payload: PayloadTaskUpdateActive, task_id: str):
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

    if not isinstance(payload.active, bool):
        return ResponseApiData(
            status="ERROR",
            data={"message": "W body nie ma klucza 'active' lub nie jest on typu boolean."},
            status_code=400,
            additional=None
        ).to_response()

    response = handler_update_task_active(user_data, task_id, payload.active)
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
