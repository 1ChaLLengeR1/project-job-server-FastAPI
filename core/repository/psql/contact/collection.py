from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.contact.response import ContactMessageResponse, _to_contact_message_response
from database.psql.database import managed_session
from database.psql.models.contact import ContactMessage


def collection_contact_messages_psql(
    application: str | None = None,
    status: str | None = None,
    db_session: Session | None = None,
) -> tuple[list[ContactMessageResponse] | None, ApiErrorData | None, bool]:
    """Wiadomości kontaktowe, najnowsze pierwsze; filtry po aplikacji i statusie."""
    try:
        with managed_session(db_session) as (db, _):
            query = db.query(ContactMessage)
            if application is not None:
                query = query.filter(ContactMessage.application == application)
            if status is not None:
                query = query.filter(ContactMessage.status == status)
            messages = query.order_by(ContactMessage.created_at.desc()).all()
            return [_to_contact_message_response(message) for message in messages], None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="collection_contact_messages_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
