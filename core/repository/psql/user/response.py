from dataclasses import dataclass

from database.psql.models.auth import Users


@dataclass
class UserResponse:
    id: str
    username: str
    type: str


def _to_user_response(model: Users) -> UserResponse:
    return UserResponse(
        id=str(model.id),
        username=model.username,
        type=model.type,
    )
