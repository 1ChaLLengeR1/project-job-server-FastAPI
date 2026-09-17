from uuid import uuid4

from sqlalchemy.orm import Session

from core.repository.psql.file.one import one_file_psql
from tests.core.repository.psql.file.helper import make_file


class TestOneFilePsql:
    def test_one01_returns_file_without_children(self, db_session: Session):
        file = make_file(db_session, name="samotny.png")

        result, err, ok = one_file_psql(str(file.id), db_session=db_session)

        assert ok is True and err is None
        assert result.file.id == str(file.id)
        assert result.children == []

    def test_one02_returns_direct_children_but_not_grandchildren(self, db_session: Session):
        parent = make_file(db_session, name="faktura.png")
        child = make_file(db_session, name="faktura-1.png", parent_file_id=str(parent.id))
        make_file(db_session, name="faktura-1-2.png", parent_file_id=str(child.id))

        result, err, ok = one_file_psql(str(parent.id), db_session=db_session)

        assert ok is True
        assert [c.name for c in result.children] == ["faktura-1.png"]

    def test_one03_not_found(self, db_session: Session):
        result, err, ok = one_file_psql(str(uuid4()), db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "NotFound"
