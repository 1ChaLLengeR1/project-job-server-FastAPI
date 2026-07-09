from core.data.response import ResponseData, create_error_response
from core.repository.psql.calendar.condition.update import update_work_condition_change_psql


def handler_update_work_condition_change(condition_id: str, norm_hours: float, hourly_rate: float) -> ResponseData:
    try:
        response_create = update_work_condition_change_psql(condition_id, norm_hours, hourly_rate)
        if not response_create["is_valid"]:
            return response_create
        return response_create

    except Exception as e:
        return create_error_response(message=f"update_work_condition_change_psql Exception - {str(e)}", status_code=500)
