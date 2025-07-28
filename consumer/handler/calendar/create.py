from consumer.data.user import UserData
from consumer.repository.psql.calendar.create import create_generator_calendar_psql
from consumer.data.response import ResponseData, create_error_response, create_success_response
from consumer.repository.psql.user.check import check_user_role_psql


def handler_create_generator_calendar(
        user_data: UserData,
        year: int,
        norm_hours: float,
        hourly_rate: float
) -> ResponseData:
    try:
        check_role = check_user_role_psql(user_data, 'superadmin')
        if not check_role['is_valid']:
            return check_role

        response_create = create_generator_calendar_psql(year, norm_hours, hourly_rate)
        if not response_create['is_valid']:
            return response_create
        return response_create
    except Exception as e:
        return create_error_response(message=str(e), status_code=500)
