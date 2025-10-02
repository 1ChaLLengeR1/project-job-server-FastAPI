from core.repository.psql.calendar.days.update import update_days_calendary_psql, update_day_calendary_by_id_psql
from core.data.response import ResponseData, create_error_response


def handler_update_day_calendary_by_id(
        day_id: str,
        norm_hours: float,
        hours_worked: float,
        hourly_rate: float,
) -> ResponseData:
    try:
        response_update = update_day_calendary_by_id_psql(day_id, norm_hours, hours_worked, hourly_rate)
        if not response_update['is_valid']:
            return response_update
        return response_update
    except Exception as e:
        return create_error_response(message=str(e), status_code=500)


def handler_update_days_calendary(
        year: int,
        month: int,
        start_day: int,
        end_day: int,
        norm_hours: float,
        hours_worked: float,
        hourly_rate: float,
) -> ResponseData:
    try:
        response_update = update_days_calendary_psql(
            year, month, start_day, end_day, norm_hours, hours_worked, hourly_rate
        )
        if not response_update['is_valid']:
            return response_update
        return response_update
    except Exception as e:
        return create_error_response(message=str(e), status_code=500)
