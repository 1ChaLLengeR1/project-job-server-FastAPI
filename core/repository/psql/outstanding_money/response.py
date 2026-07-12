from dataclasses import dataclass
from datetime import date

from database.psql.models.outstanding_money import NamesOverdue, OutStandingMoney


@dataclass
class OutstandingItemResponse:
    id: str
    amount: float
    name: str
    date: date | None
    id_name: str


@dataclass
class NamesOverdueResponse:
    id: str
    name: str


@dataclass
class OverdueListResponse:
    id_name: str
    name_overdue: str
    array_items: list[OutstandingItemResponse]
    full_price: float


@dataclass
class CreatedListResponse:
    names_overdue: NamesOverdueResponse
    new_outstanding_money: list[OutstandingItemResponse]


@dataclass
class DeletedListResponse:
    name_overdue: NamesOverdueResponse
    outstanding_money: list[OutstandingItemResponse]


def _to_outstanding_item_response(model: OutStandingMoney) -> OutstandingItemResponse:
    return OutstandingItemResponse(
        id=str(model.id),
        amount=model.amount,
        name=model.name,
        date=model.date,
        id_name=str(model.id_name),
    )


def _to_names_overdue_response(model: NamesOverdue) -> NamesOverdueResponse:
    return NamesOverdueResponse(id=str(model.id), name=model.name)
