from uuid import uuid4

from sqlalchemy.orm import Session

from core.repository.psql.file.node.delete import delete_files_node_psql
from tests.core.repository.psql.file.node.helper import make_files_node


class TestDeleteFilesNodePsql:
    def test_delete01_deletes_and_returns_snapshot(self, db_session: Session):
        node = make_files_node(db_session, name="Mama")

        result, err, ok = delete_files_node_psql(str(node.id), db_session=db_session)

        assert ok is True and err is None
        assert result.name == "Mama"

    def test_delete02_not_found(self, db_session: Session):
        result, err, ok = delete_files_node_psql(str(uuid4()), db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "NotFound"

    def test_delete03_restrict_blocks_with_child_node(self, db_session: Session):
        parent = make_files_node(db_session, name="Praca 2025-2026")
        make_files_node(db_session, name="Faktura", parent_id=str(parent.id))

        result, err, ok = delete_files_node_psql(str(parent.id), db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "IntegrityError"
