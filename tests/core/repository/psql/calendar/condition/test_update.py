from sqlalchemy.orm import Session

from core.repository.psql.calendar.condition.update import update_work_condition_change_psql
from tests.core.repository.psql.calendar.helper import make_condition


class TestUpdateWorkConditionPsql:
    def test_update01_changes_values(self, db_session: Session):
        condition = make_condition(db_session, norm_hours=8, hourly_rate=30)

        result, err, ok = update_work_condition_change_psql(str(condition.id), 7.5, 35.0, db_session=db_session)

        assert ok is True and err is None
        assert result.norm_hours == 7.5
        assert result.hourly_rate == 35.0

    def test_update02_not_found_returns_not_found(self, db_session: Session):
        result, err, ok = update_work_condition_change_psql(
            "6fa459ea-ee8a-4ca4-894e-db77e160355e", 8, 30, db_session=db_session
        )

        assert ok is False and result is None
        assert err.key_type_error == "NotFound"
