from fastapi import Request
from typing import Optional, cast
from api.gateways.types.tasks.create import ApplicationGatewayTaskCreateResult
from api.tasks.schemas import PayloadTaskCreate
from core.data.response import Error
from core.data.user import UserData

from core.helper.headers import check_required_headers


def application_gateway_task_create(request: Request, payload: PayloadTaskCreate) -> tuple[
    Optional[ApplicationGatewayTaskCreateResult], Optional[Error], bool, int]:
    try:

        required_headers = ["UserData"]
        data_header = check_required_headers(request, required_headers)
        if not data_header['is_valid']:
            return None, Error(message=data_header['data']['message']), False, data_header['status_code']

        user_data = cast(UserData, data_header['data'][0]['data'])

        if payload.description is None or not isinstance(payload.description, str) or payload.description.strip() == "":
            return None, Error(message="Pole 'description' nie może być puste ani nullem."), False, 422

        if payload.time is None or not isinstance(payload.time, int):
            return None, Error(message="Pole 'time' musi być liczbą całkowitą."), False, 422

        if payload.time <= 0:
            return None, Error(message="Pole 'time' musi być większe od zera."), False, 422

        if payload.active is None or not isinstance(payload.active, bool):
            return None, Error(message="Pole 'active' musi być typu boolean (true/false)."), False, 422

        result: ApplicationGatewayTaskCreateResult = {
            "description": payload.description,
            "time": payload.time,
            "active": payload.active,
            "user_data": user_data
        }
        return result, None, True, 200

    except Exception as e:
        return None, Error(message=str(e)), False, 417
