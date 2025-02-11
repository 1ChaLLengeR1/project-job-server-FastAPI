from fastapi import APIRouter, Request, Depends
from api.routers import CALCULATOR
from consumer.data.response import ResponseApiData
from consumer.handler.patryk.calculator_work.calculator import handler_calculations
from consumer.helper.headers import check_required_headers
from consumer.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from .schemas import CalculatorParams

router = APIRouter()


@router.post(CALCULATOR, dependencies=[Depends(JWTBasicAuthenticationMiddleware())])
def calculator_update_keys(request: Request, payload: CalculatorParams):
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

    data_dict = {
        "gross_sales": payload.gross_sales,
        "gross_purchase": payload.gross_purchase,
        "provision": payload.provision,
        "distinction": payload.distinction,
        "referrer": payload.referrer,
    }

    response = handler_calculations(user_data, data_dict)
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
