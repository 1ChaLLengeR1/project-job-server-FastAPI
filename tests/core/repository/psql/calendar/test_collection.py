from datetime import date

from sqlalchemy.orm import Session

from core.repository.psql.calendar.collection import collection_calendar_psql
from tests.core.repository.psql.calendar.helper import make_work_day


class TestCollectionCalendarPsql:
    def test_collection01_returns_days_for_month(self, db_session: Session):
        make_work_day(db_session, day=date(2030, 1, 10), hours_worked=8, hourly_rate=30)
        make_work_day(db_session, day=date(2030, 1, 11), hours_worked=6, hourly_rate=30)
        make_work_day(db_session, day=date(2030, 2, 1))  # inny miesiąc

        result, err, ok = collection_calendar_psql(2030, 1, db_session=db_session)

        assert ok is True and err is None
        assert result.year == 2030 and result.month == 1
        assert result.month_name == "Styczeń"
        assert len(result.days) == 2
        assert result.statistics.total_hours_worked == 14
        assert result.statistics.total_salary == 14 * 30

    def test_collection02_days_have_names_and_daily_salary(self, db_session: Session):
        make_work_day(db_session, day=date(2030, 1, 10), hours_worked=8, hourly_rate=25)  # czwartek

        result, _, ok = collection_calendar_psql(2030, 1, db_session=db_session)

        assert ok is True
        day = result.days[0]
        assert day.day_name == "czwartek"
        assert day.day_number == 10
        assert day.daily_salary == 200

    def test_collection03_empty_month_returns_not_found(self, db_session: Session):
        result, err, ok = collection_calendar_psql(2030, 6, db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "NotFound"
