from core.data.user import UserData
from core.repository.psql.calendar.condition.create import create_work_condition_change_psql
from core.data.response import ResponseData, create_error_response
from core.repository.psql.user.check import check_user_role_psql


def handler_create_work_condition_change(
        user_data: UserData,
        norm_hours: float,
        hourly_rate: float
) -> ResponseData:
    try:
        check_role = check_user_role_psql(user_data, 'superadmin')
        if not check_role['is_valid']:
            return check_role

        response_create = create_work_condition_change_psql(norm_hours, hourly_rate)
        if not response_create['is_valid']:
            return response_create
        return response_create

    except Exception as e:
        return create_error_response(
            message=f"handler_create_work_condition_change Exception - {str(e)}",
            status_code=500
        )
