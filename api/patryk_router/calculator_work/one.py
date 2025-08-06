from fastapi import APIRouter, Request, Depends
from api.routers import CALCULATOR_KEYS
from core.data.response import ResponseApiData
from core.handler.patryk.calculator_work.one import handler_one_calculator_keys
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware

router = APIRouter()


@router.get(CALCULATOR_KEYS, dependencies=[Depends(JWTBasicAuthenticationMiddleware())])
def calculator_keys(request: Request):
    response = handler_one_calculator_keys()
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
