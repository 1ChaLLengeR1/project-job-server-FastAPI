from core.data.response import ResponseData
from core.data.fuel_calculation.calculation import FuelData
from core.repository.psql.fuel_calculator.calculation import fuel_calculation_psql


def handler_fuel_calculation(payload: FuelData) -> ResponseData:
    try:
        response_calculation = fuel_calculation_psql(payload)
        if not response_calculation['is_valid']:
            return ResponseData(
                is_valid=response_calculation['is_valid'],
                status=response_calculation['status'],
                data=response_calculation['data'],
                status_code=response_calculation['status_code'],
                additional=response_calculation['additional'],
            )

        return ResponseData(
            is_valid=response_calculation['is_valid'],
            status=response_calculation['status'],
            data=response_calculation['data'],
            status_code=response_calculation['status_code'],
            additional=response_calculation['additional'],
        )
    except Exception as e:
        return ResponseData(
            is_valid=False,
            status="ERROR",
            data=str(e),
            status_code=500,
            additional=None
        )
