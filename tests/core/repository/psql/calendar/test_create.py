from datetime import date

from sqlalchemy.orm import Session

from core.repository.psql.calendar.create import create_generator_calendar_psql
from tests.core.repository.psql.calendar.helper import make_condition, make_work_day

YEAR = 2030  # rok w przyszłości — hours_worked dla dni roboczych ma być None


class TestCreateGeneratorCalendarPsql:
    def test_create01_generates_full_year(self, db_session: Session):
        make_condition(db_session, norm_hours=8, hourly_rate=30)

        result, err, ok = create_generator_calendar_psql(YEAR, set(), db_session=db_session)

        assert ok is True and err is None
        assert result.inserted_count == 365
        assert result.summary.year == YEAR
        assert result.summary.total_days == 365
        assert result.summary.days_before_today == 0
        assert result.summary.total_weekends + result.summary.working_days == 365

    def test_create02_weekend_has_zeros_workday_has_condition_values(self, db_session: Session):
        make_condition(db_session, norm_hours=7.5, hourly_rate=25)

        result, _, ok = create_generator_calendar_psql(YEAR, set(), db_session=db_session)

        assert ok is True
        weekend = next(d for d in result.calendar_days if d.is_weekend)
        workday = next(d for d in result.calendar_days if not d.is_weekend)
        assert weekend.norm_hours == 0 and weekend.hourly_rate == 0 and weekend.hours_worked == 0
        assert workday.norm_hours == 7.5 and workday.hourly_rate == 25 and workday.hours_worked is None

    def test_create03_marks_holidays_from_input_set(self, db_session: Session):
        make_condition(db_session)
        holiday = date(YEAR, 5, 1)

        result, _, ok = create_generator_calendar_psql(YEAR, {holiday}, db_session=db_session)

        assert ok is True
        day = next(d for d in result.calendar_days if d.date == holiday)
        assert day.is_holiday is True
        assert result.summary.total_holidays == 1

    def test_create04_no_condition_returns_not_found(self, db_session: Session):
        result, err, ok = create_generator_calendar_psql(YEAR, set(), db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "NotFound"

    def test_create05_existing_year_returns_integrity_error(self, db_session: Session):
        make_condition(db_session)
        make_work_day(db_session, day=date(YEAR, 3, 15))

        result, err, ok = create_generator_calendar_psql(YEAR, set(), db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "IntegrityError"
