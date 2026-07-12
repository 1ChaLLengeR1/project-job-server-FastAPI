from api.response import ApiErrorData
from core.service.fuel_calculator.response import FuelCalculationResponse


def calculation_fuel(
    way: float, fuel: float, combustion: float, remaining_values: float
) -> tuple[FuelCalculationResponse | None, ApiErrorData | None, bool]:
    try:
        price = ((combustion / 100) * fuel * way) + remaining_values
        pattern = f"({combustion} / 100) * {fuel} * {way} + {remaining_values}"

        return FuelCalculationResponse(price=price, pattern=pattern), None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="calculation_fuel",
            type_error="exception",
            key_type_error="Exception",
        ), False
