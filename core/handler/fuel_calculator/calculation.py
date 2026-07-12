from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.logs.create import create_logs_psql
from core.service.fuel_calculator.calculation import calculation_fuel
from core.service.fuel_calculator.response import FuelCalculationResponse


def handler_fuel_calculation(
    user_id: str,
    way: float,
    fuel: float,
    combustion: float,
    remaining_values: float,
    db_session: Session | None = None,
) -> tuple[FuelCalculationResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = calculation_fuel(way, fuel, combustion, remaining_values)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "fuel_calculator:calculation", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_fuel_calculation",
            type_error="exception",
            key_type_error="Exception",
        ), False
