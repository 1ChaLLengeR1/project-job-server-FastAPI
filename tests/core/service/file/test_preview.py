from unittest.mock import patch

from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.service.file.preview import preview_file_service
from database.psql.models.file import FileStatus
from tests.core.repository.psql.file.helper import make_file


class TestPreviewFileService:
    def test_preview01_returns_inline_presigned_url_with_configured_expiry(self, db_session: Session):
        file = make_file(db_session, status=FileStatus.COMPLETED)

        with patch(
            "core.service.file.preview.generate_get_presigned_url",
            return_value=("https://signed.example/preview", None, True),
        ) as mocked:
            result, err, ok = preview_file_service(str(file.id), db_session=db_session)

        assert ok is True and err is None
        assert result.url == "https://signed.example/preview"
        assert result.expires_in_seconds == 180
        mocked.assert_called_once_with(
            s3_key=file.s3_key, expires_seconds=180, disposition="inline", filename=file.original_name
        )

    def test_preview02_blocks_pending_file_without_calling_s3(self, db_session: Session):
        file = make_file(db_session, status=FileStatus.PENDING)

        with patch("core.service.file.preview.generate_get_presigned_url") as mocked:
            result, err, ok = preview_file_service(str(file.id), db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "IntegrityError"
        mocked.assert_not_called()

    def test_preview03_propagates_s3_failure(self, db_session: Session):
        file = make_file(db_session, status=FileStatus.COMPLETED)
        s3_error = ApiErrorData(
            message="boom", type_module="generate_get_presigned_url", type_error="exception", key_type_error="Exception"
        )

        with patch("core.service.file.preview.generate_get_presigned_url", return_value=(None, s3_error, False)):
            result, err, ok = preview_file_service(str(file.id), db_session=db_session)

        assert ok is False and result is None
        assert err is s3_error
