from uuid import uuid4

from sqlalchemy.orm import Session

from core.repository.psql.file.node.one import one_files_node_psql
from tests.core.repository.psql.file.node.helper import make_files_node


class TestOneFilesNodePsql:
    def test_one01_returns_node(self, db_session: Session):
        node = make_files_node(db_session, name="Ja", description="Mój katalog")

        result, err, ok = one_files_node_psql(str(node.id), db_session=db_session)

        assert ok is True and err is None
        assert result.node.id == str(node.id)
        assert result.node.name == "Ja"
        assert result.node.description == "Mój katalog"

    def test_one02_returns_node_with_parent_id(self, db_session: Session):
        parent = make_files_node(db_session, name="Praca 2025-2026")
        child = make_files_node(db_session, name="Faktura", parent_id=str(parent.id))

        result, err, ok = one_files_node_psql(str(child.id), db_session=db_session)

        assert ok is True
        assert result.node.parent_id == str(parent.id)

    def test_one03_not_found(self, db_session: Session):
        result, err, ok = one_files_node_psql(str(uuid4()), db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "NotFound"
        assert err.type_module == "one_files_node_psql"

    def test_one04_breadcrumb_for_root_node_has_only_itself(self, db_session: Session):
        node = make_files_node(db_session, name="Mama")

        result, err, ok = one_files_node_psql(str(node.id), db_session=db_session)

        assert ok is True
        assert [item.name for item in result.breadcrumb] == ["Mama"]

    def test_one05_breadcrumb_orders_root_to_node_across_multiple_levels(self, db_session: Session):
        root = make_files_node(db_session, name="Praca 2025-2026")
        middle = make_files_node(db_session, name="Faktury", parent_id=str(root.id))
        leaf = make_files_node(db_session, name="Faktura 3", parent_id=str(middle.id))

        result, err, ok = one_files_node_psql(str(leaf.id), db_session=db_session)

        assert ok is True
        assert [item.name for item in result.breadcrumb] == ["Praca 2025-2026", "Faktury", "Faktura 3"]
        assert [item.id for item in result.breadcrumb] == [str(root.id), str(middle.id), str(leaf.id)]
