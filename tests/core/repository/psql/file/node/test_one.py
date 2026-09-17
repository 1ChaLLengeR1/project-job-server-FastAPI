from uuid import uuid4

from sqlalchemy.orm import Session

from core.repository.psql.file.node.one import one_files_node_psql
from tests.core.repository.psql.file.node.helper import make_files_node


class TestOneFilesNodePsql:
    def test_one01_returns_node(self, db_session: Session):
        node = make_files_node(db_session, name="Ja", description="Mój katalog")

        result, err, ok = one_files_node_psql(str(node.id), db_session=db_session)

        assert ok is True and err is None
        assert result.id == str(node.id)
        assert result.name == "Ja"
        assert result.description == "Mój katalog"

    def test_one02_returns_node_with_parent_id(self, db_session: Session):
        parent = make_files_node(db_session, name="Praca 2025-2026")
        child = make_files_node(db_session, name="Faktura", parent_id=str(parent.id))

        result, err, ok = one_files_node_psql(str(child.id), db_session=db_session)

        assert ok is True
        assert result.parent_id == str(parent.id)

    def test_one03_not_found(self, db_session: Session):
        result, err, ok = one_files_node_psql(str(uuid4()), db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "NotFound"
        assert err.type_module == "one_files_node_psql"
