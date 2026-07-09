import uuid
from datetime import date

from sqlalchemy.orm import Session

from database.psql.models.outstanding_money import NamesOverdue, OutStandingMoney


def make_overdue_list(db: Session, *, name: str | None = None) -> NamesOverdue:
    overdue = NamesOverdue(id=uuid.uuid4(), name=name or f"lista_{uuid.uuid4().hex[:8]}")
    db.add(overdue)
    db.flush()
    return overdue


def make_item(
    db: Session,
    *,
    id_name: uuid.UUID,
    amount: float = 100.0,
    name: str | None = None,
    day: date | None = None,
) -> OutStandingMoney:
    item = OutStandingMoney(
        amount=amount,
        name=name or f"pozycja_{uuid.uuid4().hex[:8]}",
        date=day or date.today(),
        id_name=id_name,
    )
    db.add(item)
    db.flush()
    return item
