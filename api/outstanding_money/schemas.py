from pydantic import BaseModel


class KeysCalculatorData(BaseModel):
    name: str
    array_object: list[dict]


class AddItemParams(BaseModel):
    id_name: str
    amount: float
    name: str
