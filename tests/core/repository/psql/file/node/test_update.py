from uuid import uuid4

from sqlalchemy.orm import Session

from core.repository.psql.file.node.update import update_files_node_psql
from tests.core.repository.psql.file.node.helper import make_files_node


class TestUpdateFilesNodePsql:
    def test_update01_changes_only_given_fields(self, db_session: Session):
        node = make_files_node(db_session, name="Mama", description="stary opis")

        result, err, ok = update_files_node_psql(str(node.id), new_description="nowy opis", db_session=db_session)

        assert ok is True and err is None
        assert result.name == "Mama"
        assert result.description == "nowy opis"

    def test_update02_sets_new_parent_id(self, db_session: Session):
        parent = make_files_node(db_session, name="Praca 2025-2026")
        node = make_files_node(db_session, name="Faktura")

        result, err, ok = update_files_node_psql(str(node.id), new_parent_id=str(parent.id), db_session=db_session)

        assert ok is True
        assert result.parent_id == str(parent.id)

    def test_update03_clear_parent_id_moves_node_to_top_level(self, db_session: Session):
        parent = make_files_node(db_session, name="Praca 2025-2026")
        child = make_files_node(db_session, name="Faktura", parent_id=str(parent.id))

        result, err, ok = update_files_node_psql(str(child.id), clear_parent_id=True, db_session=db_session)

        assert ok is True and err is None
        assert result.parent_id is None

    def test_update04_not_found(self, db_session: Session):
        result, err, ok = update_files_node_psql(str(uuid4()), new_name="x", db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "NotFound"
