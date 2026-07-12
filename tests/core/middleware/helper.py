import uuid

from core.repository.psql.user.response import UserResponse

USER_ID = str(uuid.uuid4())


def make_user_response(*, user_id: str = USER_ID, username: str = "tester", type: str = "user") -> UserResponse:
    return UserResponse(id=user_id, username=username, type=type)


def user_found(user: UserResponse):
    """Wynik one_user_by_id_psql: user istnieje."""
    return user, None, True


def user_not_found():
    """Wynik one_user_by_id_psql: brak usera (tuple z NotFound)."""
    return None, None, False
