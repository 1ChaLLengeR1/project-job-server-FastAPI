from core.data.response import ResponseData, create_error_response
from core.repository.psql.calendar.condition.create import create_work_condition_change_psql


def handler_create_work_condition_change(norm_hours: float, hourly_rate: float) -> ResponseData:
    try:
        response_create = create_work_condition_change_psql(norm_hours, hourly_rate)
        if not response_create["is_valid"]:
            return response_create
        return response_create

    except Exception as e:
        return create_error_response(
            message=f"handler_create_work_condition_change Exception - {str(e)}", status_code=500
        )
