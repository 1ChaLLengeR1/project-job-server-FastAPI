from core.repository.psql.calendar.collection import collection_calendar_psql
from core.data.response import ResponseData, create_error_response


def handler_collection_calendar(
        year: int,
        month: int
) -> ResponseData:
    try:
        response_create = collection_calendar_psql(year, month)
        if not response_create['is_valid']:
            return response_create
        return response_create
    except Exception as e:
        return create_error_response(message=str(e), status_code=500)
