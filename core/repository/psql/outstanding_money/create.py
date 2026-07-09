import uuid
from datetime import date

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.outstanding_money.response import (
    CreatedListResponse,
    NamesOverdueResponse,
    OutstandingItemResponse,
    _to_outstanding_item_response,
)
from database.psql.database import managed_session
from database.psql.models.outstanding_money import NamesOverdue, OutStandingMoney


def create_list_psql(
    name: str, items: list[dict], db_session: Session | None = None
) -> tuple[CreatedListResponse | None, ApiErrorData | None, bool]:
    """`items` to zwalidowane w payloadzie pozycje: [{"amount": float, "name": str}, ...]."""
    try:
        with managed_session(db_session) as (db, _):
            new_uuid4 = uuid.uuid4()

            new_names_overdue = NamesOverdue(id=new_uuid4, name=name)
            db.add(new_names_overdue)

            new_items: list[OutstandingItemResponse] = []
            for item in items:
                new_outstanding_money = OutStandingMoney(
                    amount=item["amount"], name=item["name"], date=date.today(), id_name=new_uuid4
                )
                db.add(new_outstanding_money)
                db.flush()
                new_items.append(_to_outstanding_item_response(new_outstanding_money))

            db.flush()

            return CreatedListResponse(
                names_overdue=NamesOverdueResponse(id=str(new_uuid4), name=name),
                new_outstanding_money=new_items,
            ), None, True
    except IntegrityError as e:
        return None, ApiErrorData(
            message=str(e.orig),
            type_module="create_list_psql",
            type_error="integrity_error",
            key_type_error="IntegrityError",
        ), False
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="create_list_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False


def add_item_psql(
    id_name: str, amount: float, name: str, db_session: Session | None = None
) -> tuple[OutstandingItemResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            row_item = db.query(NamesOverdue).filter(NamesOverdue.id == id_name).first()
            if not row_item:
                return None, ApiErrorData(
                    message=f"Not found item with this id_name: {id_name}",
                    type_module="add_item_psql",
                    type_error="not_found",
                    key_type_error="NotFound",
                ), False

            new_item = OutStandingMoney(amount=amount, name=name, date=date.today(), id_name=row_item.id)
            db.add(new_item)
            db.flush()
            db.refresh(new_item)

            return _to_outstanding_item_response(new_item), None, True
    except IntegrityError as e:
        return None, ApiErrorData(
            message=str(e.orig),
            type_module="add_item_psql",
            type_error="integrity_error",
            key_type_error="IntegrityError",
        ), False
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="add_item_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
