from typing import TypedDict


class EditListParams(TypedDict, total=False):
    id: str
    name: str


class EditItem(TypedDict, total=False):
    id: str
    amount: float
    name: str
