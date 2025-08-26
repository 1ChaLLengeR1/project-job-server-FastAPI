from core.data.user import UserData
from core.repository.psql.calendar.condition.delete import delete_work_condition_change_psql
from core.data.response import ResponseData, create_error_response
from core.repository.psql.user.check import check_user_role_psql


def handler_delete_work_condition_change(
        user_data: UserData,
        condition_id: str
) -> ResponseData:
    try:
        check_role = check_user_role_psql(user_data, 'superadmin')
        if not check_role['is_valid']:
            return check_role

        response_delete = delete_work_condition_change_psql(condition_id)
        if not response_delete['is_valid']:
            return response_delete
        return response_delete

    except Exception as e:
        return create_error_response(
            message=f"handler_delete_work_condition_change Exception - {str(e)}",
            status_code=500
        )