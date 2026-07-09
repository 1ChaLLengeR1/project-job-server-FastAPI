from api.gateways.types.calendar.condition.delete import ApplicationGatewayCalendarConditionDeleteResult
from api.validators import is_valid_uuid
from core.data.response import Error


def application_gateway_calendar_condition_delete(
    condition_id: str,
) -> tuple[ApplicationGatewayCalendarConditionDeleteResult | None, Error | None, bool, int]:
    try:
        if not is_valid_uuid(condition_id):
            return None, Error(message="Pole 'condition_id' musi być prawidłowym UUID."), False, 422

        result: ApplicationGatewayCalendarConditionDeleteResult = {"condition_id": condition_id}
        return result, None, True, 200
    except Exception as e:
        return None, Error(message=str(e)), False, 400
