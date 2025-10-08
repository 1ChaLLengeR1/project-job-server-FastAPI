from core.repository.psql.calendar.condition.collection import collection_work_condition_changes_psql
from core.data.response import ResponseData, create_error_response


def handler_collection_work_condition_changes() -> ResponseData:
    try:
        response_create = collection_work_condition_changes_psql()
        if not response_create['is_valid']:
            return response_create
        return response_create
    except Exception as e:
        return create_error_response(
            message=f"collection_work_condition_changes_psql Exception - {str(e)}",
            status_code=500
        )
