from sqlalchemy.orm import Session

from core.repository.psql.tasks.create import create_task_psql


class TestCreateTaskPsql:
    def test_create01_returns_ok_with_fields(self, db_session: Session):
        result, err, ok = create_task_psql("nowy task", 45, True, db_session=db_session)

        assert ok is True and err is None
        assert result.id is not None
        assert result.description == "nowy task"
        assert result.time == 45
        assert result.active is True
        assert result.created_at is not None

    def test_create02_active_false(self, db_session: Session):
        result, err, ok = create_task_psql("wykonany", 10, False, db_session=db_session)

        assert ok is True
        assert result.active is False
