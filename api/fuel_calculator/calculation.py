from fastapi import APIRouter, Request, Depends
from api.routers import FUEL_CALCULATION
from core.data.response import ResponseApiData
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from core.handler.fuel_calculator.calculation import handler_fuel_calculation
from .schemas import FuelData

router = APIRouter()


@router.post(FUEL_CALCULATION, dependencies=[Depends(JWTBasicAuthenticationMiddleware())])
def fuel_calculation(request: Request, payload: FuelData):
    data = {
        'way': payload.way,
        'fuel': payload.fuel,
        'combustion': payload.combustion,
        'remaining_values': payload.remaining_values
    }

    response = handler_fuel_calculation(data)
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
