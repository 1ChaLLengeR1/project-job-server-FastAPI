from uuid import uuid4

from sqlalchemy.orm import Session

from core.repository.psql.file.node.collection import collection_files_nodes_psql
from tests.core.repository.psql.file.node.helper import make_files_node


class TestCollectionFilesNodesPsql:
    def test_collection01_returns_top_level_nodes_ordered_by_name(self, db_session: Session):
        make_files_node(db_session, name="Mama")
        make_files_node(db_session, name="Ja")

        result, err, ok = collection_files_nodes_psql(db_session=db_session)

        assert ok is True and err is None
        assert [node.name for node in result] == ["Ja", "Mama"]

    def test_collection02_returns_only_children_of_given_parent(self, db_session: Session):
        parent = make_files_node(db_session, name="Praca 2025-2026")
        make_files_node(db_session, name="Faktura 1", parent_id=str(parent.id))
        make_files_node(db_session, name="Faktura 2", parent_id=str(parent.id))
        make_files_node(db_session, name="Poza drzewem")

        result, err, ok = collection_files_nodes_psql(parent_id=str(parent.id), db_session=db_session)

        assert ok is True
        assert {node.name for node in result} == {"Faktura 1", "Faktura 2"}

    def test_collection03_empty_list_when_no_children(self, db_session: Session):
        result, err, ok = collection_files_nodes_psql(parent_id=str(uuid4()), db_session=db_session)

        assert ok is True and err is None
        assert result == []
