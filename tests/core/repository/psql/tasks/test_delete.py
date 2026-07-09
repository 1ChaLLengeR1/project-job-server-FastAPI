from sqlalchemy.orm import Session

from core.repository.psql.tasks.delete import delete_task_psql
from database.psql.models.tasks import Tasks
from tests.core.repository.psql.tasks.helper import make_task


class TestDeleteTaskPsql:
    def test_delete01_removes_row_and_returns_deleted_data(self, db_session: Session):
        task = make_task(db_session, description="do usuniecia")

        result, err, ok = delete_task_psql(str(task.id), db_session=db_session)

        assert ok is True and err is None
        assert result.description == "do usuniecia"
        assert db_session.query(Tasks).filter(Tasks.id == task.id).first() is None

    def test_delete02_not_found_returns_not_found(self, db_session: Session):
        result, err, ok = delete_task_psql("6fa459ea-ee8a-4ca4-894e-db77e160355e", db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "NotFound"
        assert err.type_module == "delete_task_psql"
