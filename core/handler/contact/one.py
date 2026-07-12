from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.contact.one import one_contact_message_psql
from core.repository.psql.contact.response import ContactMessageResponse
from core.repository.psql.logs.create import create_logs_psql


def handler_one_contact_message(
    user_id: str, message_id: str, db_session: Session | None = None
) -> tuple[ContactMessageResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = one_contact_message_psql(message_id, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "contact:one_message", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_one_contact_message",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
