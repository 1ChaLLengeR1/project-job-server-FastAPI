from api.calendar.condition.schema import PayloadCalendarConditionCreate
from api.gateways.types.calendar.condition.update import ApplicationGatewayCalendarConditionUpdateResult
from api.validators import is_valid_uuid
from core.data.response import Error


def application_gateway_calendar_condition_update(
    condition_id: str, payload: PayloadCalendarConditionCreate
) -> tuple[ApplicationGatewayCalendarConditionUpdateResult | None, Error | None, bool, int]:
    try:
        if not is_valid_uuid(condition_id):
            return None, Error(message="Pole 'condition_id' musi być prawidłowym UUID."), False, 422

        if payload.norm_hours is None or not isinstance(payload.norm_hours, (int, float)):
            return None, Error(message="Pole 'norm_hours' musi być liczbą."), False, 422

        if payload.norm_hours <= 0:
            return None, Error(message="Pole 'norm_hours' musi być większe od zera."), False, 422

        if payload.hourly_rate is None or not isinstance(payload.hourly_rate, (int, float)):
            return None, Error(message="Pole 'hourly_rate' musi być liczbą."), False, 422

        if payload.hourly_rate <= 0:
            return None, Error(message="Pole 'hourly_rate' musi być większe od zera."), False, 422

        result: ApplicationGatewayCalendarConditionUpdateResult = {
            "norm_hours": float(payload.norm_hours),
            "hourly_rate": float(payload.hourly_rate),
            "condition_id": condition_id,
        }
        return result, None, True, 200
    except Exception as e:
        return None, Error(message=str(e)), False, 417
