from uuid import uuid4

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.repository.psql.file.assign import assign_file_psql
from database.psql.models.file import FileStatus
from tests.core.repository.psql.file.helper import make_file
from tests.core.repository.psql.file.node.helper import make_files_node


class TestAssignFilePsql:
    def test_assign01_completed_file_gets_confirmed_with_node(self, db_session: Session):
        file = make_file(db_session, status=FileStatus.COMPLETED)
        node = make_files_node(db_session, name="Mama")

        result, err, ok = assign_file_psql(str(file.id), str(node.id), db_session=db_session)

        assert ok is True and err is None
        assert result.node_id == str(node.id)
        assert result.status == FileStatus.CONFIRMED

    def test_assign02_with_parent_file_id(self, db_session: Session):
        file = make_file(db_session, status=FileStatus.COMPLETED)
        node = make_files_node(db_session, name="Praca 2025-2026")
        parent_file = make_file(db_session, status=FileStatus.COMPLETED, node_id=str(node.id))

        result, err, ok = assign_file_psql(
            str(file.id), str(node.id), parent_file_id=str(parent_file.id), db_session=db_session
        )

        assert ok is True
        assert result.parent_file_id == str(parent_file.id)

    def test_assign03_wrong_status_returns_integrity_error(self, db_session: Session):
        file = make_file(db_session, status=FileStatus.PENDING)
        node = make_files_node(db_session, name="Mama")

        result, err, ok = assign_file_psql(str(file.id), str(node.id), db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "IntegrityError"

    def test_assign04_not_found(self, db_session: Session):
        node = make_files_node(db_session, name="Mama")

        result, err, ok = assign_file_psql(str(uuid4()), str(node.id), db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "NotFound"


class TestFilesConfirmedRequiresNodeCheckConstraint:
    def test_confirmed_without_node_id_violates_check_constraint(self, db_session: Session):
        with pytest.raises(IntegrityError):
            make_file(db_session, status=FileStatus.CONFIRMED)
