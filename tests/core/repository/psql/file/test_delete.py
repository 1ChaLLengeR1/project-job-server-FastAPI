from uuid import uuid4

from sqlalchemy.orm import Session

from core.repository.psql.file.delete import delete_file_psql
from database.psql.models.file import File
from tests.core.repository.psql.file.helper import make_file


class TestDeleteFilePsql:
    def test_delete01_deletes_and_returns_snapshot(self, db_session: Session):
        file = make_file(db_session, name="do_usuniecia.png")

        result, err, ok = delete_file_psql(str(file.id), db_session=db_session)

        assert ok is True and err is None
        assert result.id == str(file.id)
        assert result.s3_key == file.s3_key
        assert result.child_s3_keys == []

    def test_delete02_not_found(self, db_session: Session):
        result, err, ok = delete_file_psql(str(uuid4()), db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "NotFound"

    def test_delete03_collects_direct_children_s3_keys_and_cascades_in_db(self, db_session: Session):
        parent = make_file(db_session, name="faktura.png")
        child1 = make_file(db_session, name="faktura-1.png", parent_file_id=str(parent.id))
        child2 = make_file(db_session, name="faktura-2.png", parent_file_id=str(parent.id))

        result, err, ok = delete_file_psql(str(parent.id), db_session=db_session)

        assert ok is True and err is None
        assert set(result.child_s3_keys) == {child1.s3_key, child2.s3_key}
        # CASCADE z bazy usunelo rekordy dzieci razem z rodzicem
        assert db_session.query(File).filter(File.id.in_([child1.id, child2.id])).count() == 0

    def test_delete04_collects_grandchildren_s3_keys_too(self, db_session: Session):
        parent = make_file(db_session, name="faktura.png")
        child = make_file(db_session, name="faktura-1.png", parent_file_id=str(parent.id))
        grandchild = make_file(db_session, name="faktura-1-2.png", parent_file_id=str(child.id))

        result, err, ok = delete_file_psql(str(parent.id), db_session=db_session)

        assert ok is True
        assert set(result.child_s3_keys) == {child.s3_key, grandchild.s3_key}
