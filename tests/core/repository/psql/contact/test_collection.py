from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from core.repository.psql.contact.collection import collection_contact_messages_psql
from tests.core.repository.psql.contact.helper import make_contact_message


class TestCollectionContactMessagesPsql:
    def test_collection01_returns_newest_first(self, db_session: Session):
        base = datetime(2026, 7, 1, 12, 0, tzinfo=timezone.utc)
        make_contact_message(db_session, first_name="Starsza", created_at=base)
        make_contact_message(db_session, first_name="Nowsza", created_at=base + timedelta(hours=1))

        result, err, ok = collection_contact_messages_psql(db_session=db_session)

        assert ok is True and err is None
        assert [message.first_name for message in result] == ["Nowsza", "Starsza"]

    def test_collection02_filters_by_application(self, db_session: Session):
        make_contact_message(db_session, application="portfolio")
        make_contact_message(db_session, application="rentals-app")

        result, err, ok = collection_contact_messages_psql(application="portfolio", db_session=db_session)

        assert ok is True
        assert len(result) == 1 and result[0].application == "portfolio"

    def test_collection03_filters_by_status(self, db_session: Session):
        make_contact_message(db_session, status="new")
        make_contact_message(db_session, status="closed")

        result, err, ok = collection_contact_messages_psql(status="closed", db_session=db_session)

        assert ok is True
        assert len(result) == 1 and result[0].status == "closed"

    def test_collection04_empty_table_returns_empty_list(self, db_session: Session):
        result, err, ok = collection_contact_messages_psql(db_session=db_session)

        assert ok is True
        assert result == []
