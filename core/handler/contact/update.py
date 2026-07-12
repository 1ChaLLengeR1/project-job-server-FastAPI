from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.contact.response import ContactMessageResponse
from core.repository.psql.contact.update import update_contact_message_status_psql
from core.repository.psql.logs.create import create_logs_psql


def handler_update_contact_message_status(
    user_id: str, message_id: str, new_status: str, db_session: Session | None = None
) -> tuple[ContactMessageResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = update_contact_message_status_psql(message_id, new_status, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "contact:update_message_status", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_update_contact_message_status",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
