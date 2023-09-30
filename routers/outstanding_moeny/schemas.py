from pydantic import BaseModel


class CreateListParams(BaseModel):
    id_user: str
    username: str
    name: str
    array_object: list = []

    class Config:
        orm_mode = True


class EditListParams(BaseModel):
    id_user: str
    username: str
    id: str
    name: str

    class Config:
        orm_mode = True


class DeleteId(BaseModel):
    id_user: str
    username: str
    id: str

    class Config:
        orm_mode = True


class AddItemParams(BaseModel):
    id_user: str
    username: str
    id_name: str
    amount: float
    name: str

    class Config:
        orm_mode = True


class EditItem(BaseModel):
    id_user: str
    username: str
    id: str
    amount: float
    name: str
