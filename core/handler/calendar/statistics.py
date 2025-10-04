from core.repository.psql.calendar.statistics import statistics_calendar_psql
from core.data.response import ResponseData, create_error_response


def handler_statistics_calendar(
        year: int,
) -> ResponseData:
    try:
        response_create = statistics_calendar_psql(year)
        if not response_create['is_valid']:
            return response_create
        return response_create
    except Exception as e:
        return create_error_response(message=str(e), status_code=500)
