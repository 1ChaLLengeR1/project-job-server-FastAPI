from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.contact.response import ContactMessageResponse, _to_contact_message_response
from database.psql.database import managed_session
from database.psql.models.contact import ContactMessage


def create_contact_message_psql(
    first_name: str,
    phone_number: str,
    description: str,
    application: str,
    last_name: str | None = None,
    email: str | None = None,
    db_session: Session | None = None,
) -> tuple[ContactMessageResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            new_message = ContactMessage(
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                email=email,
                description=description,
                application=application,
                status="new",
            )
            db.add(new_message)
            db.flush()
            db.refresh(new_message)
            return _to_contact_message_response(new_message), None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="create_contact_message_psql",
                type_error="integrity_error",
                key_type_error="IntegrityError",
            ),
            False,
        )
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="create_contact_message_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
