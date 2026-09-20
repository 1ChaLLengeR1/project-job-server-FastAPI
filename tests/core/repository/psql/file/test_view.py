from uuid import uuid4

from sqlalchemy.orm import Session

from core.repository.psql.file.view import get_viewable_file_psql
from database.psql.models.file import FileStatus
from tests.core.repository.psql.file.helper import make_file
from tests.core.repository.psql.file.node.helper import make_files_node


class TestGetViewableFilePsql:
    def test_view01_returns_file_when_completed(self, db_session: Session):
        file = make_file(db_session, status=FileStatus.COMPLETED)

        result, err, ok = get_viewable_file_psql(str(file.id), db_session=db_session)

        assert ok is True and err is None
        assert result.id == str(file.id)

    def test_view02_returns_file_when_confirmed(self, db_session: Session):
        node = make_files_node(db_session, name="Mama")
        file = make_file(db_session, status=FileStatus.CONFIRMED, node_id=str(node.id))

        result, err, ok = get_viewable_file_psql(str(file.id), db_session=db_session)

        assert ok is True

    def test_view03_blocks_pending_file(self, db_session: Session):
        file = make_file(db_session, status=FileStatus.PENDING)

        result, err, ok = get_viewable_file_psql(str(file.id), db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "IntegrityError"

    def test_view04_blocks_failed_file(self, db_session: Session):
        file = make_file(db_session, status=FileStatus.FAILED)

        result, err, ok = get_viewable_file_psql(str(file.id), db_session=db_session)

        assert ok is False
        assert err.key_type_error == "IntegrityError"

    def test_view05_not_found(self, db_session: Session):
        result, err, ok = get_viewable_file_psql(str(uuid4()), db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "NotFound"
