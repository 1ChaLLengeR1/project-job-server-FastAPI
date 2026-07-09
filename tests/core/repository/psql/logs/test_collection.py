from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from core.repository.psql.logs.collection import collection_logs_psql
from tests.core.repository.psql.logs.helper import make_log


class TestCollectionLogsPsql:
    def test_collection01_zero_returns_all_logs(self, db_session: Session):
        make_log(db_session, description="tasks:create")
        make_log(db_session, description="tasks:delete")

        result, err, ok = collection_logs_psql(0, db_session=db_session)

        assert ok is True and err is None
        assert len(result) == 2

    def test_collection02_limit_and_order_newest_first(self, db_session: Session):
        now = datetime.now(timezone.utc)
        make_log(db_session, description="stary", date=now - timedelta(hours=2))
        make_log(db_session, description="nowy", date=now)
        make_log(db_session, description="sredni", date=now - timedelta(hours=1))

        result, err, ok = collection_logs_psql(2, db_session=db_session)

        assert ok is True
        assert len(result) == 2
        assert [log.description for log in result] == ["nowy", "sredni"]

    def test_collection03_empty_table_returns_empty_list(self, db_session: Session):
        result, err, ok = collection_logs_psql(0, db_session=db_session)

        assert ok is True and result == []
