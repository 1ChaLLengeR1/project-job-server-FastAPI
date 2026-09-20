from sqlalchemy.orm import Session

from core.repository.psql.file.node.create import create_files_node_psql
from tests.core.repository.psql.file.node.helper import make_files_node


class TestCreateFilesNodePsql:
    def test_create01_returns_ok_with_fields(self, db_session: Session):
        result, err, ok = create_files_node_psql("Mama", description="Dokumenty mamy", db_session=db_session)

        assert ok is True and err is None
        assert result.id is not None
        assert result.name == "Mama"
        assert result.description == "Dokumenty mamy"
        assert result.parent_id is None
        assert result.is_active is True

    def test_create02_with_parent_id(self, db_session: Session):
        parent = make_files_node(db_session, name="Ja")

        result, err, ok = create_files_node_psql("Faktury", parent_id=str(parent.id), db_session=db_session)

        assert ok is True and err is None
        assert result.parent_id == str(parent.id)

    def test_create03_duplicate_name_same_parent_integrity_error(self, db_session: Session):
        parent = make_files_node(db_session, name="Praca 2025-2026")
        make_files_node(db_session, name="Faktura", parent_id=str(parent.id))

        result, err, ok = create_files_node_psql("Faktura", parent_id=str(parent.id), db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "IntegrityError"
