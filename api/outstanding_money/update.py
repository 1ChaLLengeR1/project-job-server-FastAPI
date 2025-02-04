from fastapi import APIRouter, Request, Depends
from api.routers import EDIT_NAME_LIST_OUTSTANDING_MONEY, EDIT_ITEM_OUTSTANDING_MONEY
from consumer.data.response import ResponseApiData
from consumer.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from consumer.handler.outstanding_moeny.update import handler_edit_name_list, handler_edit_item
from consumer.helper.headers import check_required_headers
from .schemas import EditListParams, EditItem

router = APIRouter()


@router.put(EDIT_NAME_LIST_OUTSTANDING_MONEY, dependencies=[Depends(JWTBasicAuthenticationMiddleware())])
def edit_name_list(request: Request, payload: EditListParams):
    required_headers = ["UserData"]
    data_header = check_required_headers(request, required_headers)
    if not data_header['is_valid']:
        return ResponseApiData(
            status="ERROR",
            data=data_header['data'],
            status_code=data_header['status_code'],
            additional=None
        ).to_response()

    user_data = data_header['data'][0]['data']

    data = {
        "id": payload.id,
        "name": payload.name
    }

    response = handler_edit_name_list(user_data, data)
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


@router.put(EDIT_ITEM_OUTSTANDING_MONEY, dependencies=[Depends(JWTBasicAuthenticationMiddleware())])
def edit_item(request: Request, payload: EditItem):
    required_headers = ["UserData"]
    data_header = check_required_headers(request, required_headers)
    if not data_header['is_valid']:
        return ResponseApiData(
            status="ERROR",
            data=data_header['data'],
            status_code=data_header['status_code'],
            additional=None
        ).to_response()

    user_data = data_header['data'][0]['data']

    data = {
        "id": payload.id,
        "amount": payload.amount,
        "name": payload.name
    }

    response = handler_edit_item(user_data, data)
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
