from consumer.data.user import UserData
from consumer.repository.psql.tasks.update import update_task_psql, update_task_active_psql
from consumer.data.response import ResponseData, create_error_response, create_success_response
from consumer.repository.psql.user.check import check_user_role_psql


def handler_update_task(user_data: UserData, task_id: str, new_description: str) -> ResponseData:
    try:
        check_role = check_user_role_psql(user_data, 'superadmin')
        if not check_role['is_valid']:
            return check_role

        response_update = update_task_psql(task_id, new_description)
        if not response_update['is_valid']:
            return response_update
        return response_update
    except Exception as e:
        return create_error_response(message=str(e), status_code=500)


def handler_update_task_active(user_data: UserData, task_id: str, new_active: bool) -> ResponseData:
    try:
        check_role = check_user_role_psql(user_data, 'superadmin')
        if not check_role['is_valid']:
            return check_role

        response_update = update_task_active_psql(task_id, new_active)
        if not response_update['is_valid']:
            return response_update
        return response_update
    except Exception as e:
        return create_error_response(message=str(e), status_code=500)
