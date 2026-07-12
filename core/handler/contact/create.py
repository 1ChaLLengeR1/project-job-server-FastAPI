from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.contact.create import create_contact_message_psql
from core.repository.psql.contact.response import ContactMessageResponse


def handler_create_contact_message(
    application: str,
    first_name: str,
    phone_number: str,
    description: str,
    last_name: str | None = None,
    email: str | None = None,
    db_session: Session | None = None,
) -> tuple[ContactMessageResponse | None, ApiErrorData | None, bool]:
    """Zapis wiadomości z publicznego formularza kontaktowego.

    BEZ audytu (create_logs_psql) — endpoint jest publiczny, nie ma usera;
    `application` pochodzi z claimu tokena kontaktowego (middleware), nie z payloadu.
    """
    try:
        result, err, ok = create_contact_message_psql(
            first_name,
            phone_number,
            description,
            application,
            last_name=last_name,
            email=email,
            db_session=db_session,
        )
        if not ok:
            return None, err, False

        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_create_contact_message",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
