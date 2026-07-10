from uuid import uuid4

from sqlalchemy.orm import Session

from core.repository.psql.contact.one import one_contact_message_psql
from tests.core.repository.psql.contact.helper import make_contact_message


class TestOneContactMessagePsql:
    def test_one01_returns_message(self, db_session: Session):
        message = make_contact_message(db_session, first_name="Jan", description="Pytanie o garaż")

        result, err, ok = one_contact_message_psql(str(message.id), db_session=db_session)

        assert ok is True and err is None
        assert result.id == str(message.id)
        assert result.description == "Pytanie o garaż"

    def test_one02_not_found(self, db_session: Session):
        result, err, ok = one_contact_message_psql(str(uuid4()), db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "NotFound"
