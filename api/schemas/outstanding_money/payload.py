from pydantic import BaseModel, Field, field_validator

from api.validators import validate_non_empty_str, validate_uuid


class CreateListItemPayload(BaseModel):
    amount: float = Field(description="Kwota pozycji")
    name: str = Field(max_length=255, description="Nazwa pozycji")

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value: str) -> str:
        return validate_non_empty_str(value)


class CreateListPayload(BaseModel):
    name: str = Field(max_length=255, description="Nazwa listy zaległości")
    array_object: list[CreateListItemPayload] = Field(description="Pozycje startowe listy")

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value: str) -> str:
        return validate_non_empty_str(value)


class AddItemPayload(BaseModel):
    id_name: str = Field(description="Id listy (UUID)")
    amount: float = Field(description="Kwota pozycji")
    name: str = Field(max_length=255, description="Nazwa pozycji")

    @field_validator("id_name")
    @classmethod
    def id_name_is_uuid(cls, value: str) -> str:
        return validate_uuid(value)

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value: str) -> str:
        return validate_non_empty_str(value)


class EditListPayload(BaseModel):
    id: str = Field(description="Id listy (UUID)")
    name: str = Field(max_length=255, description="Nowa nazwa listy")

    @field_validator("id")
    @classmethod
    def id_is_uuid(cls, value: str) -> str:
        return validate_uuid(value)

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value: str) -> str:
        return validate_non_empty_str(value)


class EditItemPayload(BaseModel):
    id: str = Field(description="Id pozycji (UUID)")
    amount: float = Field(description="Nowa kwota pozycji")
    name: str = Field(max_length=255, description="Nowa nazwa pozycji")

    @field_validator("id")
    @classmethod
    def id_is_uuid(cls, value: str) -> str:
        return validate_uuid(value)

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value: str) -> str:
        return validate_non_empty_str(value)
