from dataclasses import dataclass
from datetime import datetime

from database.psql.models.contact import ContactMessage

VALID_MESSAGE_STATUSES = ("new", "read", "closed")


@dataclass
class ContactMessageResponse:
    id: str
    first_name: str
    last_name: str | None
    phone_number: str
    email: str | None
    description: str
    application: str
    status: str
    created_at: datetime | None
    updated_at: datetime | None


def _to_contact_message_response(model: ContactMessage) -> ContactMessageResponse:
    return ContactMessageResponse(
        id=str(model.id),
        first_name=model.first_name,
        last_name=model.last_name,
        phone_number=model.phone_number,
        email=model.email,
        description=model.description,
        application=model.application,
        status=model.status,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )
