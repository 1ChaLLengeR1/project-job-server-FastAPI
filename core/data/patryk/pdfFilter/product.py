from typing import TypedDict


class ProductData(TypedDict, total=False):
    index: int
    column_excel: int
    lp: int
    name: str
    quantity: int
    ean: str
    location: str | None
