from typing import TypedDict, Union, Dict, Any, List, Literal, Optional


class EditListParams(TypedDict, total=False):
    id: str
    name: str


class EditItem(TypedDict, total=False):
    id: str
    amount: float
    name: str
