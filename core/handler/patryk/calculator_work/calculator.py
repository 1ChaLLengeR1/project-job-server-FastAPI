from core.data.response import ResponseData
from core.repository.psql.patryk.calculator import calculations_psql
from core.data.patryk.calculator.calculator import CalculatorData
from core.data.user import UserData


def handler_calculations(user_data: UserData, payload: CalculatorData):
    try:
        if payload['gross_sales'] == 0 or payload['gross_purchase'] == 0:
            return ResponseData(
                is_valid=False,
                status="ERROR",
                data=str(f"gross_sales and gross_purchase can't by 0"),
                status_code=400,
                additional=None
            )

        response = calculations_psql(user_data, payload)
        if not response['is_valid']:
            return ResponseData(
                is_valid=response['is_valid'],
                status=response['status'],
                data=response['data'],
                status_code=response['status_code'],
                additional=response['additional']
            )

        return ResponseData(
            is_valid=response['is_valid'],
            status=response['status'],
            data=response['data'],
            status_code=response['status_code'],
            additional=response['additional']
        )

    except Exception as e:
        return ResponseData(
            is_valid=False,
            status="ERROR",
            data=str(e),
            status_code=500,
            additional=None
        )
