from typing import TypedDict


class CreateListParams(TypedDict, total=False):
    name: str
    array_object: list[dict]


class AddItemParams(TypedDict, total=False):
    id_name: str
    amount: float
    name: str
