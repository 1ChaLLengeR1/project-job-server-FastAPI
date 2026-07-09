from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.logs.create import create_logs_psql
from core.repository.psql.outstanding_money.delete import delete_item_psql, delete_list_psql
from core.repository.psql.outstanding_money.response import DeletedListResponse, OutstandingItemResponse


def handler_delete_list(
    user_id: str, list_id: str, db_session: Session | None = None
) -> tuple[DeletedListResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = delete_list_psql(list_id, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "outstanding_money:delete_list", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_delete_list",
            type_error="exception",
            key_type_error="Exception",
        ), False


def handler_delete_item(
    user_id: str, item_id: str, db_session: Session | None = None
) -> tuple[OutstandingItemResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = delete_item_psql(item_id, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "outstanding_money:delete_item", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_delete_item",
            type_error="exception",
            key_type_error="Exception",
        ), False
