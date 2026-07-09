from core.data.response import ResponseData, create_error_response
from core.repository.psql.calendar.condition.delete import delete_work_condition_change_psql


def handler_delete_work_condition_change(condition_id: str) -> ResponseData:
    try:
        response_delete = delete_work_condition_change_psql(condition_id)
        if not response_delete["is_valid"]:
            return response_delete
        return response_delete

    except Exception as e:
        return create_error_response(
            message=f"handler_delete_work_condition_change Exception - {str(e)}", status_code=500
        )
