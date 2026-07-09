from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.logs.create import create_logs_psql
from core.repository.psql.outstanding_money.create import add_item_psql, create_list_psql
from core.repository.psql.outstanding_money.response import CreatedListResponse, OutstandingItemResponse


def handler_create_list(
    user_id: str, name: str, items: list[dict], db_session: Session | None = None
) -> tuple[CreatedListResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = create_list_psql(name, items, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "outstanding_money:create_list", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_create_list",
            type_error="exception",
            key_type_error="Exception",
        ), False


def handler_add_item(
    user_id: str, id_name: str, amount: float, name: str, db_session: Session | None = None
) -> tuple[OutstandingItemResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = add_item_psql(id_name, amount, name, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "outstanding_money:add_item", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_add_item",
            type_error="exception",
            key_type_error="Exception",
        ), False
