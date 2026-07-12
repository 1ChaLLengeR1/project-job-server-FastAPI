from dataclasses import dataclass

from database.psql.models.auth import Users


@dataclass
class UserResponse:
    id: str
    username: str
    type: str


@dataclass
class UserCredentialsResponse:
    id: str
    username: str
    type: str
    password: str  # hash bcrypt — tylko do weryfikacji w handlerze logowania


def _to_user_response(model: Users) -> UserResponse:
    return UserResponse(
        id=str(model.id),
        username=model.username,
        type=model.type,
    )


def _to_user_credentials_response(model: Users) -> UserCredentialsResponse:
    return UserCredentialsResponse(
        id=str(model.id),
        username=model.username,
        type=model.type,
        password=model.password,
    )
