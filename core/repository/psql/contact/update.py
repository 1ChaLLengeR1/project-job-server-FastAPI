from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.contact.response import (
    VALID_MESSAGE_STATUSES,
    ContactMessageResponse,
    _to_contact_message_response,
)
from database.psql.database import managed_session
from database.psql.models.contact import ContactMessage


def update_contact_message_status_psql(
    message_id: str, new_status: str, db_session: Session | None = None
) -> tuple[ContactMessageResponse | None, ApiErrorData | None, bool]:
    """Zmiana statusu obsługi wiadomości: new | read | closed."""
    try:
        if new_status not in VALID_MESSAGE_STATUSES:
            return (
                None,
                ApiErrorData(
                    message=f"Nieznany status wiadomości: '{new_status}'",
                    type_module="update_contact_message_status_psql",
                    type_error="exception",
                    key_type_error="Exception",
                ),
                False,
            )

        with managed_session(db_session) as (db, _):
            message = db.query(ContactMessage).filter(ContactMessage.id == message_id).first()
            if not message:
                return (
                    None,
                    ApiErrorData(
                        message=f"Wiadomość kontaktowa nie istnieje: {message_id}",
                        type_module="update_contact_message_status_psql",
                        type_error="not_found",
                        key_type_error="NotFound",
                    ),
                    False,
                )

            message.status = new_status
            db.flush()
            db.refresh(message)
            return _to_contact_message_response(message), None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="update_contact_message_status_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
