from unittest.mock import patch

from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.service.file.delete import delete_file_service
from tests.core.repository.psql.file.helper import make_file


class TestDeleteFileService:
    def test_delete01_deletes_record_and_s3_object_for_file_without_children(self, db_session: Session):
        file = make_file(db_session, name="solo.png")

        with patch("core.service.file.delete.delete_file_s3", return_value=(True, None, True)) as mocked_delete:
            result, err, ok = delete_file_service(str(file.id), db_session=db_session)

        assert ok is True and err is None
        assert result.file_id == str(file.id)
        mocked_delete.assert_called_once_with(s3_key=file.s3_key)

    def test_delete02_cascade_deletes_s3_objects_of_all_children(self, db_session: Session):
        parent = make_file(db_session, name="faktura.png")
        child = make_file(db_session, name="faktura-1.png", parent_file_id=str(parent.id))
        parent_s3_key, child_s3_key = parent.s3_key, child.s3_key

        with patch("core.service.file.delete.delete_file_s3", return_value=(True, None, True)) as mocked_delete:
            result, err, ok = delete_file_service(str(parent.id), db_session=db_session)

        assert ok is True and err is None
        called_keys = {call.kwargs["s3_key"] for call in mocked_delete.call_args_list}
        assert called_keys == {parent_s3_key, child_s3_key}

    def test_delete03_missing_child_s3_object_is_not_treated_as_failure(self, db_session: Session):
        parent = make_file(db_session, name="faktura.png")
        make_file(db_session, name="faktura-1.png", parent_file_id=str(parent.id))
        parent_s3_key = parent.s3_key

        def fake_delete(s3_key):
            if s3_key == parent_s3_key:
                return True, None, True
            return None, ApiErrorData(
                message="not found", type_module="delete_file_s3", type_error="not_found", key_type_error="NotFound"
            ), False

        with patch("core.service.file.delete.delete_file_s3", side_effect=fake_delete):
            result, err, ok = delete_file_service(str(parent.id), db_session=db_session)

        assert ok is True and err is None

    def test_delete04_real_s3_failure_on_child_fails_whole_operation(self, db_session: Session):
        parent = make_file(db_session, name="faktura.png")
        make_file(db_session, name="faktura-1.png", parent_file_id=str(parent.id))
        parent_s3_key = parent.s3_key

        def fake_delete(s3_key):
            if s3_key == parent_s3_key:
                return True, None, True
            return None, ApiErrorData(
                message="boom", type_module="delete_file_s3", type_error="exception", key_type_error="Exception"
            ), False

        with patch("core.service.file.delete.delete_file_s3", side_effect=fake_delete):
            result, err, ok = delete_file_service(str(parent.id), db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "S3DeleteFailed"
