from datetime import datetime
from core.repository.psql.tasks.statistics import get_task_statistics_psql
from core.data.response import ResponseData, create_error_response, create_success_response


def handler_get_task_statistics_task(start_date: datetime, end_date: datetime) -> ResponseData:
    try:
        response_statistics = get_task_statistics_psql(start_date, end_date)
        if not response_statistics['is_valid']:
            return response_statistics
        return response_statistics
    except Exception as e:
        return create_error_response(message=str(e), status_code=500)
