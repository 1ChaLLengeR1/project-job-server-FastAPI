from uuid import uuid4

from sqlalchemy.orm import Session

from core.repository.psql.file.create import create_file_psql
from database.psql.models.file import FileStatus, FileType
from tests.core.repository.psql.user.helper import create_test_user


class TestCreateFilePsql:
    def test_create01_returns_ok_with_fields_and_default_pending_status(self, db_session: Session):
        s3_key = f"tests/{uuid4().hex}.png"

        result, err, ok = create_file_psql(
            user_id=None,
            name="wewnetrzna_nazwa.png",
            original_name="zdjecie.png",
            size=2048,
            file_type=FileType.PHOTO,
            mime_type="image/png",
            s3_key=s3_key,
            s3_prefix="tests",
            db_session=db_session,
        )

        assert ok is True and err is None
        assert result.name == "wewnetrzna_nazwa.png"
        assert result.original_name == "zdjecie.png"
        assert result.size == 2048
        assert result.file_type == FileType.PHOTO
        assert result.mime_type == "image/png"
        assert result.s3_key == s3_key
        assert result.s3_prefix == "tests"
        assert result.status == FileStatus.PENDING
        assert result.user_id is None
        assert result.url is None

    def test_create02_accepts_real_user_id(self, db_session: Session):
        user = create_test_user(db_session)

        result, err, ok = create_file_psql(
            user_id=str(user.id),
            name="a.png",
            original_name="a.png",
            size=1,
            file_type=FileType.PHOTO,
            mime_type="image/png",
            s3_key=f"tests/{uuid4().hex}.png",
            s3_prefix="tests",
            db_session=db_session,
        )

        assert ok is True
        assert result.user_id == str(user.id)

    def test_create03_duplicate_s3_key_integrity_error(self, db_session: Session):
        s3_key = f"tests/{uuid4().hex}.png"
        create_file_psql(
            user_id=None,
            name="pierwszy.png",
            original_name="pierwszy.png",
            size=1,
            file_type=FileType.PHOTO,
            mime_type="image/png",
            s3_key=s3_key,
            s3_prefix="tests",
            db_session=db_session,
        )

        result, err, ok = create_file_psql(
            user_id=None,
            name="drugi.png",
            original_name="drugi.png",
            size=1,
            file_type=FileType.PHOTO,
            mime_type="image/png",
            s3_key=s3_key,
            s3_prefix="tests",
            db_session=db_session,
        )

        assert ok is False and result is None
        assert err.key_type_error == "IntegrityError"
