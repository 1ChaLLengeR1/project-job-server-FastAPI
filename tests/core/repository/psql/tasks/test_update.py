from sqlalchemy.orm import Session

from core.repository.psql.tasks.update import update_task_active_psql, update_task_psql
from tests.core.repository.psql.tasks.helper import make_task


class TestUpdateTaskPsql:
    def test_update01_changes_description_and_time(self, db_session: Session):
        task = make_task(db_session, description="stary", time=10)

        result, err, ok = update_task_psql(str(task.id), "nowy opis", 20, db_session=db_session)

        assert ok is True and err is None
        assert result.description == "nowy opis"
        assert result.time == 20

    def test_update02_not_found_returns_not_found(self, db_session: Session):
        result, err, ok = update_task_psql(
            "6fa459ea-ee8a-4ca4-894e-db77e160355e", "x", 1, db_session=db_session
        )

        assert ok is False and result is None
        assert err.key_type_error == "NotFound"
        assert err.type_module == "update_task_psql"


class TestUpdateTaskActivePsql:
    def test_update_active01_changes_flag(self, db_session: Session):
        task = make_task(db_session, active=True)

        result, err, ok = update_task_active_psql(str(task.id), False, db_session=db_session)

        assert ok is True and err is None
        assert result.active is False

    def test_update_active02_not_found_returns_not_found(self, db_session: Session):
        result, err, ok = update_task_active_psql(
            "6fa459ea-ee8a-4ca4-894e-db77e160355e", True, db_session=db_session
        )

        assert ok is False
        assert err.key_type_error == "NotFound"
