from consumer.data.response import ResponseData, create_error_response, create_success_response
from database.db import get_db
from consumer.data.user import UserData
from database.auth.models import Users
from typing import Literal


def check_user_role_psql(user_data: UserData, type_role: Literal['superadmin', 'admin', 'guest']) -> ResponseData:
    db = next(get_db())
    try:
        role = ['superadmin', 'admin', 'guest']

        row_user = db.query(Users).filter(Users.id == user_data['id'], Users.username == user_data['username']).first()
        if not row_user:
            return create_error_response(
                message=f"Not found user with this params: username{user_data['username']} and id: {user_data['id']}",
                status_code=403)

        if row_user.type == role[0]:
            return create_success_response(data=None, status_code=200)

        if row_user.type != type_role:
            return create_error_response(
                message=f"This user: {row_user.username} have not permission!",
                status_code=403)

        return create_success_response(data=None, status_code=200)

    except Exception as e:
        return create_error_response(message=str(e), status_code=471)

    finally:
        db.close()
