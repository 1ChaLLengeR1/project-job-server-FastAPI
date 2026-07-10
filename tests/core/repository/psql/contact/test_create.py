from sqlalchemy.orm import Session

from core.repository.psql.contact.create import create_contact_message_psql
from database.psql.models.contact import ContactMessage


class TestCreateContactMessagePsql:
    def test_create01_creates_message_with_default_status_new(self, db_session: Session):
        result, err, ok = create_contact_message_psql(
            "Jan",
            "+48 500 600 700",
            "Pytanie o wycenę",
            "portfolio",
            last_name="Kowalski",
            email="jan@example.com",
            db_session=db_session,
        )

        assert ok is True and err is None
        assert result.first_name == "Jan" and result.last_name == "Kowalski"
        assert result.email == "jan@example.com"
        assert result.application == "portfolio"
        assert result.status == "new"
        assert db_session.query(ContactMessage).count() == 1

    def test_create02_optional_fields_can_be_none(self, db_session: Session):
        result, err, ok = create_contact_message_psql(
            "Ania", "500600700", "Proszę o kontakt", "rentals-app", db_session=db_session
        )

        assert ok is True
        assert result.last_name is None and result.email is None
