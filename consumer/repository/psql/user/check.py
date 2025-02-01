from consumer.data.response import ResponseData
from database.db import get_db
from consumer.data.user import UserData
from database.auth.models import Users
from typing import Literal


def check_user_role_psql(user_data: UserData, type_role: Literal['superadmin', 'admin', 'guest']) -> ResponseData:
    db_gen = get_db()
    db = next(db_gen)
    try:
        role = ['superadmin', 'admin', 'guest']

        row_user = db.query(Users).filter(Users.id == user_data['id'], Users.username == user_data['username']).first()
        if not row_user:
            ResponseData(
                is_valid=False,
                status="ERROR",
                data=str(f"Not found user with this params: username{user_data['username']} and id: {user_data['id']}"),
                status_code=400,
                additional=None
            )

        if row_user.type == role[0]:
            return ResponseData(
                is_valid=True,
                status="SUCCESS",
                data=None,
                status_code=200,
                additional=None
            )

        if row_user.type != type_role:
            return ResponseData(
                is_valid=False,
                status="ERROR",
                data=str(f"This user: {row_user.username} have not permission!"),
                status_code=401,
                additional=None
            )

        return ResponseData(
            is_valid=True,
            status="SUCCESS",
            data=None,
            status_code=200,
            additional=None
        )

    except Exception as e:
        return ResponseData(
            is_valid=False,
            status="ERROR",
            data=str(e),
            status_code=417,
            additional=None
        )
    finally:
        db.close()
