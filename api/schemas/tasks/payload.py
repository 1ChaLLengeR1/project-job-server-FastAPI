from pydantic import BaseModel, Field, field_validator

from api.validators import validate_non_empty_str


class TaskCreatePayload(BaseModel):
    description: str = Field(max_length=255, description="Opis taska")
    time: int = Field(gt=0, description="Czas w minutach, większy od zera")
    active: bool = Field(default=True, description="Czy task jest aktywny")

    @field_validator("description")
    @classmethod
    def description_not_empty(cls, value: str) -> str:
        return validate_non_empty_str(value)


class TaskUpdatePayload(BaseModel):
    description: str = Field(max_length=255, description="Nowy opis taska")
    time: int = Field(gt=0, description="Nowy czas w minutach, większy od zera")

    @field_validator("description")
    @classmethod
    def description_not_empty(cls, value: str) -> str:
        return validate_non_empty_str(value)


class TaskUpdateActivePayload(BaseModel):
    active: bool = Field(description="Nowy stan aktywności taska")
