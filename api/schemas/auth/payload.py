from pydantic import BaseModel, Field, field_validator

from api.validators import validate_non_empty_str


class LoginPayload(BaseModel):
    username: str = Field(max_length=255, description="Nazwa użytkownika")
    password: str = Field(max_length=255, description="Hasło")

    @field_validator("username", "password")
    @classmethod
    def not_empty(cls, value: str) -> str:
        return validate_non_empty_str(value)
