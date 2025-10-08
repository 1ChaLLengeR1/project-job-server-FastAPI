from core.data.user import UserData
from core.repository.psql.tasks.delete import delete_task_psql
from core.data.response import ResponseData, create_error_response, create_success_response
from core.repository.psql.user.check import check_user_role_psql


def handler_delete_task(user_data: UserData, task_id: str) -> ResponseData:
    try:
        check_role = check_user_role_psql(user_data, 'superadmin')
        if not check_role['is_valid']:
            return check_role

        response_delete = delete_task_psql(task_id)
        if not response_delete['is_valid']:
            return response_delete
        return response_delete
    except Exception as e:
        return create_error_response(message=str(e), status_code=500)
