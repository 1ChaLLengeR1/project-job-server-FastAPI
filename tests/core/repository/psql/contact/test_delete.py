from uuid import uuid4

from sqlalchemy.orm import Session

from core.repository.psql.contact.delete import delete_contact_message_psql
from database.psql.models.contact import ContactMessage
from tests.core.repository.psql.contact.helper import make_contact_message


class TestDeleteContactMessagePsql:
    def test_delete01_deletes_and_returns_snapshot(self, db_session: Session):
        message = make_contact_message(db_session, first_name="Jan")

        result, err, ok = delete_contact_message_psql(str(message.id), db_session=db_session)

        assert ok is True and err is None
        assert result.first_name == "Jan"
        assert db_session.query(ContactMessage).count() == 0

    def test_delete02_not_found(self, db_session: Session):
        result, err, ok = delete_contact_message_psql(str(uuid4()), db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"
