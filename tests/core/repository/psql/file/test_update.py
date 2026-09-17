from datetime import date

from sqlalchemy.orm import Session

from core.repository.psql.file.update import update_file_psql
from database.psql.models.file import FileStatus
from tests.core.repository.psql.file.helper import make_file
from tests.core.repository.psql.file.node.helper import make_files_node


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
        result, err, ok = update_file_psql("6fa459ea-ee8a-4ca4-894e-db77e160355e", new_name="x", db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "NotFound"
        assert err.type_module == "update_file_psql"

    def test_update04_sets_node_id_and_parent_file_id(self, db_session: Session):
        node = make_files_node(db_session, name="Mama")
        parent_file = make_file(db_session, status=FileStatus.CONFIRMED, node_id=str(node.id))
        file = make_file(db_session, status=FileStatus.COMPLETED)

        result, err, ok = update_file_psql(
            str(file.id), new_node_id=str(node.id), new_parent_file_id=str(parent_file.id), db_session=db_session
        )

        assert ok is True and err is None
        assert result.node_id == str(node.id)
        assert result.parent_file_id == str(parent_file.id)

    def test_update05_clear_parent_file_id(self, db_session: Session):
        node = make_files_node(db_session, name="Mama")
        parent_file = make_file(db_session, status=FileStatus.CONFIRMED, node_id=str(node.id))
        file = make_file(
            db_session, status=FileStatus.CONFIRMED, node_id=str(node.id), parent_file_id=str(parent_file.id)
        )

        result, err, ok = update_file_psql(str(file.id), clear_parent_file_id=True, db_session=db_session)

        assert ok is True and err is None
        assert result.parent_file_id is None

    def test_update06_sets_and_clears_description(self, db_session: Session):
        file = make_file(db_session, description="stary opis")

        set_result, _, set_ok = update_file_psql(str(file.id), new_description="nowy opis", db_session=db_session)
        assert set_ok is True
        assert set_result.description == "nowy opis"

        clear_result, _, clear_ok = update_file_psql(str(file.id), clear_description=True, db_session=db_session)
        assert clear_ok is True
        assert clear_result.description is None

    def test_update07_sets_and_clears_guarantee_dates(self, db_session: Session):
        file = make_file(db_session)

        set_result, _, set_ok = update_file_psql(
            str(file.id),
            new_guarantee_start_date=date(2026, 1, 1),
            new_guarantee_end_date=date(2028, 1, 1),
            db_session=db_session,
        )
        assert set_ok is True
        assert set_result.guarantee_start_date == date(2026, 1, 1)
        assert set_result.guarantee_end_date == date(2028, 1, 1)

        clear_result, _, clear_ok = update_file_psql(
            str(file.id), clear_guarantee_start_date=True, clear_guarantee_end_date=True, db_session=db_session
        )
        assert clear_ok is True
        assert clear_result.guarantee_start_date is None
        assert clear_result.guarantee_end_date is None
