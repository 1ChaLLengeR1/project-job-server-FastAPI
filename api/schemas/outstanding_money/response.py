from datetime import date

from pydantic import BaseModel


class OutstandingItemData(BaseModel):
    id: str
    amount: float
    name: str
    date: date | None
    id_name: str


class NamesOverdueData(BaseModel):
    id: str
    name: str


class OverdueListData(BaseModel):
    id_name: str
    name_overdue: str
    array_items: list[OutstandingItemData]
    full_price: float


class CreatedListData(BaseModel):
    names_overdue: NamesOverdueData
    new_outstanding_money: list[OutstandingItemData]


class DeletedListData(BaseModel):
    name_overdue: NamesOverdueData
    outstanding_money: list[OutstandingItemData]
