from uuid import uuid4

from sqlalchemy.orm import Session

from core.repository.psql.file.node.delete import delete_files_node_psql
from database.psql.models.file import FileStatus
from tests.core.repository.psql.file.helper import make_file
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

        # regresja: w realnym requeście get_db() commituje sesję po zwróceniu
        # odpowiedzi (nawet dla 409) - bez rollbacku w managed_session()
        # (bug naprawiony w database/psql/database.py) ten commit wybuchał
        # PendingRollbackError, maskując poprawną odpowiedź 409 błędem 500
        db_session.commit()

    def test_delete04_blocks_with_assigned_file_with_clear_message(self, db_session: Session):
        node = make_files_node(db_session, name="Mama")
        make_file(db_session, status=FileStatus.CONFIRMED, node_id=str(node.id))

        result, err, ok = delete_files_node_psql(str(node.id), db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "IntegrityError"
        assert "przypisane pliki" in err.message

    def test_delete05_allows_delete_after_last_file_unlinked(self, db_session: Session):
        node = make_files_node(db_session, name="Mama")
        file = make_file(db_session, status=FileStatus.CONFIRMED, node_id=str(node.id))
        # confirmed => node_id NOT NULL (ck_files_confirmed_requires_node) - realny "unassign"
        # zmienia tez status, nie tylko czysci node_id.
        file.status = FileStatus.COMPLETED
        file.node_id = None
        db_session.flush()

        result, err, ok = delete_files_node_psql(str(node.id), db_session=db_session)

        assert ok is True and err is None
