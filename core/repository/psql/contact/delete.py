from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.contact.response import ContactMessageResponse, _to_contact_message_response
from database.psql.database import managed_session
from database.psql.models.contact import ContactMessage


def delete_contact_message_psql(
    message_id: str, db_session: Session | None = None
) -> tuple[ContactMessageResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            message = db.query(ContactMessage).filter(ContactMessage.id == message_id).first()
            if not message:
                return (
                    None,
                    ApiErrorData(
                        message=f"Wiadomość kontaktowa nie istnieje: {message_id}",
                        type_module="delete_contact_message_psql",
                        type_error="not_found",
                        key_type_error="NotFound",
                    ),
                    False,
                )

            snapshot = _to_contact_message_response(message)
            db.delete(message)
            db.flush()
            return snapshot, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="delete_contact_message_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
