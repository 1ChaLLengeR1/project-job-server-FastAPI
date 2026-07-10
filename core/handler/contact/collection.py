from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.contact.collection import collection_contact_messages_psql
from core.repository.psql.contact.response import ContactMessageResponse
from core.repository.psql.logs.create import create_logs_psql


def handler_collection_contact_messages(
    user_id: str,
    application: str | None = None,
    status: str | None = None,
    db_session: Session | None = None,
) -> tuple[list[ContactMessageResponse] | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = collection_contact_messages_psql(application, status, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "contact:collection_messages", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_collection_contact_messages",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
