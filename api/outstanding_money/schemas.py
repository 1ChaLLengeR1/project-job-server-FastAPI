from pydantic import BaseModel


class KeysCalculatorData(BaseModel):
    name: str
    array_object: list[dict]


class AddItemParams(BaseModel):
    id_name: str
    amount: float
    name: str


class EditListParams(BaseModel):
    id: str
    name: str


class EditItem(BaseModel):
    id: str
    amount: float
    name: str
