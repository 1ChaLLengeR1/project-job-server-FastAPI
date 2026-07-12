from sqlalchemy.orm import Session

from core.repository.psql.logs.create import create_logs_psql
from tests.core.repository.psql.user.helper import create_test_user


class TestCreateLogsPsql:
    def test_create01_returns_ok_with_username_from_db(self, db_session: Session):
        user = create_test_user(db_session)

        result, err, ok = create_logs_psql(str(user.id), "tasks:create", db_session=db_session)

        assert ok is True and err is None
        assert result.id is not None
        assert result.username == user.username
        assert result.description == "tasks:create"
        assert result.date is not None

    def test_create02_missing_user_returns_not_found(self, db_session: Session):
        result, err, ok = create_logs_psql(
            "6fa459ea-ee8a-4ca4-894e-db77e160355e", "tasks:create", db_session=db_session
        )

        assert ok is False and result is None
        assert err.key_type_error == "NotFound"
        assert err.type_module == "create_logs_psql"
