from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.logs.create import create_logs_psql
from core.repository.psql.outstanding_money.response import NamesOverdueResponse, OutstandingItemResponse
from core.repository.psql.outstanding_money.update import edit_item_psql, edit_name_list_psql


def handler_edit_name_list(
    user_id: str, list_id: str, name: str, db_session: Session | None = None
) -> tuple[NamesOverdueResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = edit_name_list_psql(list_id, name, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "outstanding_money:edit_name_list", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_edit_name_list",
            type_error="exception",
            key_type_error="Exception",
        ), False


def handler_edit_item(
    user_id: str, item_id: str, amount: float, name: str, db_session: Session | None = None
) -> tuple[OutstandingItemResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = edit_item_psql(item_id, amount, name, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "outstanding_money:edit_item", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_edit_item",
            type_error="exception",
            key_type_error="Exception",
        ), False
