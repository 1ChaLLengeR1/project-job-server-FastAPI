from datetime import date

from sqlalchemy.orm import Session

from core.repository.psql.calendar.condition.create import create_work_condition_change_psql


class TestCreateWorkConditionPsql:
    def test_create01_returns_ok_with_today_start_date(self, db_session: Session):
        result, err, ok = create_work_condition_change_psql(8.0, 32.5, db_session=db_session)

        assert ok is True and err is None
        assert result.id is not None
        assert result.norm_hours == 8.0
        assert result.hourly_rate == 32.5
        assert result.start_date == date.today()
        assert result.created_at is not None
