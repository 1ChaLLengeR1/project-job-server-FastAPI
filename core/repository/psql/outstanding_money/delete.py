from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.outstanding_money.response import (
    DeletedListResponse,
    OutstandingItemResponse,
    _to_names_overdue_response,
    _to_outstanding_item_response,
)
from database.psql.database import managed_session
from database.psql.models.outstanding_money import NamesOverdue, OutStandingMoney


def delete_list_psql(
    list_id: str, db_session: Session | None = None
) -> tuple[DeletedListResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            item_names_overdue = db.query(NamesOverdue).filter(NamesOverdue.id == list_id).first()
            if not item_names_overdue:
                return None, ApiErrorData(
                    message=f"Not found item_names_overdue with this id: {list_id}",
                    type_module="delete_list_psql",
                    type_error="not_found",
                    key_type_error="NotFound",
                ), False

            item_outstanding_money = db.query(OutStandingMoney).filter(OutStandingMoney.id_name == list_id).all()

            deleted = DeletedListResponse(
                name_overdue=_to_names_overdue_response(item_names_overdue),
                outstanding_money=[_to_outstanding_item_response(item) for item in item_outstanding_money],
            )

            db.delete(item_names_overdue)
            for item in item_outstanding_money:
                db.delete(item)
            db.flush()

            return deleted, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="delete_list_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False


def delete_item_psql(
    item_id: str, db_session: Session | None = None
) -> tuple[OutstandingItemResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            row_out_standing_money = db.query(OutStandingMoney).filter(OutStandingMoney.id == item_id).first()
            if not row_out_standing_money:
                return None, ApiErrorData(
                    message=f"Not found out_standing_money with this id: {item_id}",
                    type_module="delete_item_psql",
                    type_error="not_found",
                    key_type_error="NotFound",
                ), False

            deleted_item = _to_outstanding_item_response(row_out_standing_money)
            db.delete(row_out_standing_money)
            db.flush()

            return deleted_item, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="delete_item_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
