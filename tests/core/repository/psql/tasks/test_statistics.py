from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from core.repository.psql.tasks.statistics import get_task_statistics_psql
from tests.core.repository.psql.tasks.helper import make_task


def _range():
    now = datetime.now(timezone.utc)
    return now - timedelta(days=1), now + timedelta(days=1)


class TestGetTaskStatisticsPsql:
    def test_statistics01_counts_only_inactive_tasks(self, db_session: Session):
        make_task(db_session, time=30, active=False)
        make_task(db_session, time=45, active=False)
        make_task(db_session, time=100, active=True)  # aktywny — nie liczy się

        start_date, end_date = _range()
        result, err, ok = get_task_statistics_psql(start_date, end_date, db_session=db_session)

        assert ok is True and err is None
        assert result.total_tasks == 2
        assert result.total_time == 75

    def test_statistics02_tasks_per_day_has_entry_for_each_day(self, db_session: Session):
        make_task(db_session, active=False)

        start_date, end_date = _range()
        result, err, ok = get_task_statistics_psql(start_date, end_date, db_session=db_session)

        assert ok is True
        assert len(result.tasks_per_day) == 3  # wczoraj, dzis, jutro
        assert sum(result.tasks_per_day.values()) == 1

    def test_statistics03_empty_range_returns_zeros(self, db_session: Session):
        start_date, end_date = _range()
        result, err, ok = get_task_statistics_psql(start_date, end_date, db_session=db_session)

        assert ok is True
        assert result.total_tasks == 0
        assert result.total_time == 0
        assert result.average_per_week == 0
