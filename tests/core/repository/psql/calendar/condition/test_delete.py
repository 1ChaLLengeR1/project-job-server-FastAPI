from sqlalchemy.orm import Session

from core.repository.psql.calendar.condition.delete import delete_work_condition_change_psql
from database.psql.models.calendar import WorkConditionChange
from tests.core.repository.psql.calendar.helper import make_condition


class TestDeleteWorkConditionPsql:
    def test_delete01_removes_row_and_returns_deleted_data(self, db_session: Session):
        condition = make_condition(db_session, norm_hours=6)

        result, err, ok = delete_work_condition_change_psql(str(condition.id), db_session=db_session)

        assert ok is True and err is None
        assert result.norm_hours == 6
        assert (
            db_session.query(WorkConditionChange).filter(WorkConditionChange.id == condition.id).first() is None
        )

    def test_delete02_not_found_returns_not_found(self, db_session: Session):
        result, err, ok = delete_work_condition_change_psql(
            "6fa459ea-ee8a-4ca4-894e-db77e160355e", db_session=db_session
        )

        assert ok is False and result is None
        assert err.key_type_error == "NotFound"
