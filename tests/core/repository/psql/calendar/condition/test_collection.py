from datetime import date, timedelta

from sqlalchemy.orm import Session

from core.repository.psql.calendar.condition.collection import collection_work_condition_changes_psql
from tests.core.repository.psql.calendar.helper import make_condition


class TestCollectionWorkConditionsPsql:
    def test_collection01_returns_newest_start_date_first(self, db_session: Session):
        today = date.today()
        make_condition(db_session, norm_hours=7, start_date=today - timedelta(days=10))
        make_condition(db_session, norm_hours=8, start_date=today)

        result, err, ok = collection_work_condition_changes_psql(db_session=db_session)

        assert ok is True and err is None
        assert [condition.norm_hours for condition in result] == [8, 7]

    def test_collection02_empty_returns_empty_list(self, db_session: Session):
        result, err, ok = collection_work_condition_changes_psql(db_session=db_session)

        assert ok is True and result == []
