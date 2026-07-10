"""Fabryka modeli domeny contact."""

from datetime import datetime

from sqlalchemy.orm import Session

from database.psql.models.contact import ContactMessage


def make_contact_message(
    db: Session,
    *,
    first_name: str = "Jan",
    last_name: str | None = "Kowalski",
    phone_number: str = "+48 500 600 700",
    email: str | None = None,
    description: str = "Pytanie o wycenę mieszkania",
    application: str = "portfolio",
    status: str = "new",
    created_at: datetime | None = None,
) -> ContactMessage:
    message = ContactMessage(
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        email=email,
        description=description,
        application=application,
        status=status,
    )
    if created_at is not None:
        # created_at ma server_default=now() wspólny dla transakcji — testy kolejności
        # potrzebują rozróżnialnych timestampów
        message.created_at = created_at
    db.add(message)
    db.flush()
    return message
