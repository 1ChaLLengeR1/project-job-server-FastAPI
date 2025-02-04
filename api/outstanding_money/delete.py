from fastapi import APIRouter, Request, Depends
from api.routers import DELETE_LIST_OUTSTANDING_MONEY, DELETE_ITEM_OUTSTANDING_MONEY
from consumer.data.response import ResponseApiData
from consumer.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from consumer.handler.outstanding_moeny.delete import handler_delete_list, handler_delete_item
from consumer.helper.headers import check_required_headers

router = APIRouter()


@router.delete(DELETE_LIST_OUTSTANDING_MONEY, dependencies=[Depends(JWTBasicAuthenticationMiddleware())])
def delete_list(request: Request, id: str):
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

    response = handler_delete_list(user_data, id)
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


@router.delete(DELETE_ITEM_OUTSTANDING_MONEY, dependencies=[Depends(JWTBasicAuthenticationMiddleware())])
def delete_item(request: Request, id: str):
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

    response = handler_delete_item(user_data, id)
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
