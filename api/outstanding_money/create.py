from typing import cast

from fastapi import APIRouter, Depends, Request

from api.routers import ADD_ITEM_OUTSTANDING_MONEY, CREATE_LIST_OUTSTANDING_MONEY
from core.data.response import ResponseApiData
from core.data.user import UserData
from core.handler.outstanding_moeny.create import handler_add_item, handler_create_list
from core.helper.headers import check_required_headers
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware

from .schemas import AddItemParams, KeysCalculatorData

router = APIRouter()


@router.post(CREATE_LIST_OUTSTANDING_MONEY, dependencies=[Depends(JWTBasicAuthenticationMiddleware())])
def create_list(request: Request, payload: KeysCalculatorData):
    required_headers = ["UserData"]
    data_header = check_required_headers(request, required_headers)
    if not data_header["is_valid"]:
        return ResponseApiData(
            status="ERROR", data=data_header["data"], status_code=data_header["status_code"], additional=None
        ).to_response()

    user_data = cast(UserData, data_header["data"][0]["data"])

    data = {"name": payload.name, "array_object": payload.array_object}

    response = handler_create_list(user_data, data)
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


@router.post(ADD_ITEM_OUTSTANDING_MONEY, dependencies=[Depends(JWTBasicAuthenticationMiddleware())])
def add_item(request: Request, payload: AddItemParams):
    required_headers = ["UserData"]
    data_header = check_required_headers(request, required_headers)
    if not data_header["is_valid"]:
        return ResponseApiData(
            status="ERROR", data=data_header["data"], status_code=data_header["status_code"], additional=None
        ).to_response()

    user_data = data_header["data"][0]["data"]

    data = {"id_name": payload.id_name, "amount": payload.amount, "name": payload.name}

    response = handler_add_item(user_data, data)
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
