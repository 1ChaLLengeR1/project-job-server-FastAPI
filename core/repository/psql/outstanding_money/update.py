from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.outstanding_money.response import (
    NamesOverdueResponse,
    OutstandingItemResponse,
    _to_names_overdue_response,
    _to_outstanding_item_response,
)
from database.psql.database import managed_session
from database.psql.models.outstanding_money import NamesOverdue, OutStandingMoney


def edit_name_list_psql(
    list_id: str, name: str, db_session: Session | None = None
) -> tuple[NamesOverdueResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            item_row = db.query(NamesOverdue).filter(NamesOverdue.id == list_id).first()
            if not item_row:
                return None, ApiErrorData(
                    message=f"Not found item with this id: {list_id}",
                    type_module="edit_name_list_psql",
                    type_error="not_found",
                    key_type_error="NotFound",
                ), False

            item_row.name = name
            db.flush()
            db.refresh(item_row)

            return _to_names_overdue_response(item_row), None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="edit_name_list_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False


def edit_item_psql(
    item_id: str, amount: float, name: str, db_session: Session | None = None
) -> tuple[OutstandingItemResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            edit_item = db.query(OutStandingMoney).filter(OutStandingMoney.id == item_id).first()
            if not edit_item:
                return None, ApiErrorData(
                    message=f"Not found edit_item with this id: {item_id}",
                    type_module="edit_item_psql",
                    type_error="not_found",
                    key_type_error="NotFound",
                ), False

            edit_item.amount = amount
            edit_item.name = name
            db.flush()
            db.refresh(edit_item)

            return _to_outstanding_item_response(edit_item), None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="edit_item_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
