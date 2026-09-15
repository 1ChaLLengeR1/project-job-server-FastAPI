from sqlalchemy.orm import Session

from core.repository.psql.file.update import update_file_psql
from database.psql.models.file import FileStatus
from tests.core.repository.psql.file.helper import make_file


class TestUpdateFilePsql:
    def test_update01_changes_only_name_when_status_is_none(self, db_session: Session):
        file = make_file(db_session, name="stary.png", status=FileStatus.PENDING)

        result, err, ok = update_file_psql(str(file.id), new_name="nowy.png", db_session=db_session)

        assert ok is True and err is None
        assert result.name == "nowy.png"
        assert result.status == FileStatus.PENDING

    def test_update02_changes_only_status_when_name_is_none(self, db_session: Session):
        file = make_file(db_session, name="bez_zmian.png", status=FileStatus.PENDING)

        result, err, ok = update_file_psql(str(file.id), new_status=FileStatus.COMPLETED, db_session=db_session)

        assert ok is True and err is None
        assert result.name == "bez_zmian.png"
        assert result.status == FileStatus.COMPLETED

    def test_update03_not_found_returns_not_found(self, db_session: Session):
        result, err, ok = update_file_psql(
            "6fa459ea-ee8a-4ca4-894e-db77e160355e", new_name="x", db_session=db_session
        )

        assert ok is False and result is None
        assert err.key_type_error == "NotFound"
        assert err.type_module == "update_file_psql"
