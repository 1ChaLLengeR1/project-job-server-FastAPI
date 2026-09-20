from sqlalchemy.orm import Session

from core.repository.psql.file.unassigned import collection_unassigned_files_psql
from database.psql.models.file import FileStatus
from tests.core.repository.psql.file.helper import make_file
from tests.core.repository.psql.file.node.helper import make_files_node


class TestCollectionUnassignedFilesPsql:
    def test_unassigned01_returns_only_completed_without_node(self, db_session: Session):
        node = make_files_node(db_session, name="Mama")
        unassigned = make_file(db_session, name="osierocony.png", status=FileStatus.COMPLETED)
        make_file(db_session, name="przypisany.png", status=FileStatus.CONFIRMED, node_id=str(node.id))
        make_file(db_session, name="pending.png", status=FileStatus.PENDING)

        result, err, ok = collection_unassigned_files_psql(db_session=db_session)

        assert ok is True and err is None
        assert [file.name for file in result.data] == ["osierocony.png"]
        assert result.data[0].id == str(unassigned.id)

    def test_unassigned02_empty_when_nothing_matches(self, db_session: Session):
        make_file(db_session, name="pending.png", status=FileStatus.PENDING)

        result, err, ok = collection_unassigned_files_psql(db_session=db_session)

        assert ok is True
        assert result.data == []
        assert result.pagination.total == 0
