from datetime import date, timedelta

from sqlalchemy.orm import Session

from core.repository.psql.calendar.days.update import (
    update_day_automatically_psql,
    update_day_calendary_by_id_psql,
    update_days_automatically_for_salary,
    update_days_calendary_psql,
)
from tests.core.repository.psql.calendar.helper import make_condition, make_work_day

MISSING_UUID = "6fa459ea-ee8a-4ca4-894e-db77e160355e"


class TestUpdateDayByIdPsql:
    def test_update_by_id01_changes_values(self, db_session: Session):
        work_day = make_work_day(db_session, day=date(2030, 1, 10), hours_worked=8, hourly_rate=30)

        result, err, ok = update_day_calendary_by_id_psql(str(work_day.id), 7.0, 5.5, 40.0, db_session=db_session)

        assert ok is True and err is None
        assert result.norm_hours == 7.0
        assert result.hours_worked == 5.5
        assert result.hourly_rate == 40.0

    def test_update_by_id02_not_found_returns_not_found(self, db_session: Session):
        result, err, ok = update_day_calendary_by_id_psql(MISSING_UUID, 8, 8, 30, db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "NotFound"


class TestUpdateDaysRangePsql:
    def test_update_range01_updates_all_days_in_range(self, db_session: Session):
        for day_number in range(10, 14):
            make_work_day(db_session, day=date(2030, 1, day_number), hours_worked=0)

        result, err, ok = update_days_calendary_psql(2030, 1, 11, 13, 8, 8, 33, db_session=db_session)

        assert ok is True and err is None
        assert result.updated_count == 3
        assert result.start_date == date(2030, 1, 11)
        assert result.end_date == date(2030, 1, 13)

    def test_update_range02_no_days_returns_not_found(self, db_session: Session):
        result, err, ok = update_days_calendary_psql(2030, 1, 1, 5, 8, 8, 30, db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "NotFound"


class TestUpdateDayAutomaticallyPsql:
    def test_auto01_fills_past_weekdays_with_condition_values(self, db_session: Session):
        make_condition(db_session, norm_hours=8, hourly_rate=30)
        # poniedziałek w przeszłości z pustymi godzinami
        past_monday = date.today() - timedelta(days=date.today().weekday() + 7)
        make_work_day(db_session, day=past_monday, hours_worked=None, norm_hours=0, hourly_rate=0)

        result, err, ok = update_day_automatically_psql(db_session=db_session)

        assert ok is True and err is None
        assert result.updated_count == 1
        updated = result.updated_days[0]
        assert updated.hours_worked == 8 and updated.norm_hours == 8 and updated.hourly_rate == 30
        assert result.condition_used.norm_hours == 8

    def test_auto02_skips_weekends_and_filled_days(self, db_session: Session):
        make_condition(db_session)
        past_monday = date.today() - timedelta(days=date.today().weekday() + 7)
        past_saturday = past_monday + timedelta(days=5)
        make_work_day(db_session, day=past_monday, hours_worked=8, norm_hours=8, hourly_rate=30)  # uzupełniony
        make_work_day(db_session, day=past_saturday, hours_worked=0, norm_hours=0, hourly_rate=0)  # weekend

        result, err, ok = update_day_automatically_psql(db_session=db_session)

        assert ok is True
        assert result.updated_count == 0

    def test_auto03_no_condition_returns_not_found(self, db_session: Session):
        result, err, ok = update_day_automatically_psql(db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "NotFound"


class TestUpdateDaysSalaryPsql:
    def test_salary01_recalculates_hourly_rate_from_salary(self, db_session: Session):
        make_work_day(db_session, day=date(2030, 1, 10), hours_worked=8, norm_hours=8, hourly_rate=30)
        make_work_day(db_session, day=date(2030, 1, 11), hours_worked=2, norm_hours=8, hourly_rate=30)

        result, err, ok = update_days_automatically_for_salary(2030, 1, 500.0, db_session=db_session)

        assert ok is True and err is None
        assert result.updated_count == 2
        assert result.total_hours_worked == 10
        assert result.calculated_hourly_rate == 50.0
        assert result.actual_total_salary == 500.0

    def test_salary02_no_working_days_returns_not_found(self, db_session: Session):
        make_work_day(db_session, day=date(2030, 2, 1), hours_worked=0, norm_hours=0)

        result, err, ok = update_days_automatically_for_salary(2030, 2, 500.0, db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "NotFound"
