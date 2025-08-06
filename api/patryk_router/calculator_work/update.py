from fastapi import APIRouter, Request, Depends
from api.routers import CALCULATOR_KEYS_UPDATE
from core.data.response import ResponseApiData
from core.handler.patryk.calculator_work.update import handler_update_calculator_keys
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from core.helper.headers import check_required_headers
from .schemas import KeysCalculatorData

router = APIRouter()


@router.put(CALCULATOR_KEYS_UPDATE, dependencies=[Depends(JWTBasicAuthenticationMiddleware())])
def calculator_update_keys(request: Request, payload: KeysCalculatorData):
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
        "id": payload.id,
        "income_tax": payload.income_tax,
        "vat": payload.vat,
        "inpost_parcel_locker": payload.inpost_parcel_locker,
        "inpost_courier": payload.inpost_courier,
        "inpost_cash_of_delivery_courier": payload.inpost_cash_of_delivery_courier,
        "dpd": payload.dpd,
        "allegro_matt": payload.allegro_matt,
        "without_smart": payload.without_smart
    }

    response = handler_update_calculator_keys(user_data, data_dict)
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
