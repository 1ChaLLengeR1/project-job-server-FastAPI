from typing import TypedDict, Union, Dict, Any, List, Literal, Optional


class CreateListParams(TypedDict, total=False):
    name: str
    array_object: list[dict]


class AddItemParams(TypedDict, total=False):
    id_name: str
    amount: float
    name: str
