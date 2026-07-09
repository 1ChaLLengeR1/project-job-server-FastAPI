from datetime import date

from sqlalchemy.orm import Session

from core.repository.psql.calendar.statistics import statistics_calendar_psql
from tests.core.repository.psql.calendar.helper import make_work_day


class TestStatisticsCalendarPsql:
    def test_statistics01_aggregates_year(self, db_session: Session):
        make_work_day(db_session, day=date(2030, 1, 10), hours_worked=8, norm_hours=8, hourly_rate=30)
        make_work_day(db_session, day=date(2030, 1, 11), hours_worked=6, norm_hours=8, hourly_rate=30)
        make_work_day(db_session, day=date(2030, 1, 12), hours_worked=0, norm_hours=8, hourly_rate=30)
        make_work_day(db_session, day=date(2030, 5, 1), hours_worked=0, norm_hours=0, is_holiday=True)

        result, err, ok = statistics_calendar_psql(2030, db_session=db_session)

        assert ok is True and err is None
        assert result.total_hours_worked == 14
        assert result.total_earnings == 14 * 30
        assert result.working_days_count == 2
        assert result.total_norm_hours == 24
        assert result.total_holidays == 1
        assert result.total_days_in_year == 4
        assert result.average_hours_per_working_day == 7.0

    def test_statistics02_empty_year_returns_zeros(self, db_session: Session):
        result, err, ok = statistics_calendar_psql(2031, db_session=db_session)

        assert ok is True
        assert result.total_days_in_year == 0
        assert result.total_hours_worked == 0
        assert result.work_efficiency_percentage == 0
