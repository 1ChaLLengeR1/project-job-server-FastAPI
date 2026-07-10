from uuid import uuid4

from sqlalchemy.orm import Session

from core.repository.psql.contact.update import update_contact_message_status_psql
from tests.core.repository.psql.contact.helper import make_contact_message


class TestUpdateContactMessageStatusPsql:
    def test_update01_changes_status(self, db_session: Session):
        message = make_contact_message(db_session, status="new")

        result, err, ok = update_contact_message_status_psql(str(message.id), "read", db_session=db_session)

        assert ok is True and err is None
        assert result.status == "read"

    def test_update02_invalid_status_rejected(self, db_session: Session):
        message = make_contact_message(db_session)

        result, err, ok = update_contact_message_status_psql(str(message.id), "archived", db_session=db_session)

        assert ok is False and result is None
        assert "archived" in err.message

    def test_update03_not_found(self, db_session: Session):
        result, err, ok = update_contact_message_status_psql(str(uuid4()), "read", db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"
