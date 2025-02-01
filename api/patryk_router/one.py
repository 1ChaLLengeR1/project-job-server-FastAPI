from fastapi import APIRouter, Request, Depends
from api.routers import CALCULATOR_KEYS
from consumer.data.response import ResponseApiData
from consumer.handler.patryk.one import handler_one_calculator_keys
from consumer.middleware.basic_authorization import JWTBasicAuthenticationMiddleware

router = APIRouter()


@router.get(CALCULATOR_KEYS, dependencies=[Depends(JWTBasicAuthenticationMiddleware())])
def calculator_keys(request: Request):
    response = handler_one_calculator_keys()
    print(response)
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
