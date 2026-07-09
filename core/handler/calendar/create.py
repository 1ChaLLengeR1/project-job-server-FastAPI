from core.data.response import ResponseData, create_error_response
from core.repository.psql.calendar.create import create_generator_calendar_psql


def handler_create_generator_calendar(year: int) -> ResponseData:
    try:
        response_create = create_generator_calendar_psql(year)
        if not response_create["is_valid"]:
            return response_create
        return response_create
    except Exception as e:
        return create_error_response(message=str(e), status_code=500)
