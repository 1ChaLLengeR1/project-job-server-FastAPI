from consumer.data.response import ResponseData
from consumer.data.fuel_calculation.calculation import FuelData


def fuel_calculation_psql(payload: FuelData) -> ResponseData:
    try:
        errors = []

        if not isinstance(payload['way'], (int, float)):
            errors.append("'way' must be a number")
        if not isinstance(payload['fuel'], (int, float)):
            errors.append("'fuel' must be a number")
        if not isinstance(payload['combustion'], (int, float)):
            errors.append("'combustion' must be a number")
        if not isinstance(payload['remaining_values'], (int, float)):
            errors.append("'remaining_values' must be a number")

        if len(errors) > 0:
            return ResponseData(
                is_valid=False,
                status="ERROR",
                data=errors,
                status_code=400,
                additional=None
            )

        price = ((payload['combustion'] / 100) * payload['fuel'] * payload['way']) + payload['remaining_values']
        pattern = f"({payload['combustion']} / 100) * {payload['fuel']} * {payload['way']} + {payload['remaining_values']}"

        data = {
            'price': price,
            'pattern': pattern
        }

        return ResponseData(
            is_valid=True,
            status="SUCCESS",
            data=data,
            status_code=200,
            additional=None
        )

    except Exception as e:
        return ResponseData(
            is_valid=False,
            status="ERROR",
            data=str(e),
            status_code=417,
            additional=None
        )
