from sqlalchemy.orm import Session

from core.repository.psql.user.one import one_user_by_id_psql, one_user_credentials_by_username_psql
from tests.core.repository.psql.user.helper import create_test_user


class TestOneUserPsql:
    def test_one01_returns_user_by_id(self, db_session: Session):
        user = create_test_user(db_session, type="admin")

        result, err, ok = one_user_by_id_psql(str(user.id), db_session=db_session)

        assert ok is True and err is None
        assert result.id == str(user.id)
        assert result.username == user.username
        assert result.type == "admin"

    def test_one02_not_found_returns_not_found(self, db_session: Session):
        result, err, ok = one_user_by_id_psql("6fa459ea-ee8a-4ca4-894e-db77e160355e", db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "NotFound"
        assert err.type_module == "one_user_by_id_psql"


class TestOneUserCredentialsPsql:
    def test_credentials01_returns_user_with_password_hash(self, db_session: Session):
        user = create_test_user(db_session, password="hash123")

        result, err, ok = one_user_credentials_by_username_psql(user.username, db_session=db_session)

        assert ok is True and err is None
        assert result.id == str(user.id)
        assert result.password == "hash123"

    def test_credentials02_not_found_returns_not_found(self, db_session: Session):
        result, err, ok = one_user_credentials_by_username_psql("nie_ma_takiego", db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "NotFound"
