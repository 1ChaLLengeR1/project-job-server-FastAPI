import uuid
from pathlib import Path

import pytest
import requests
from sqlalchemy.orm import Session

from config.settings import settings
from core.infra.s3.config import get_s3_client
from core.infra.s3.delete import delete_file_s3
from core.infra.s3.init import initialization_url_upload_file
from database.psql.models.file import File, FileType
from tests.core.repository.psql.user.helper import create_test_user

IMAGE_PATH = Path(__file__).resolve().parents[3] / "files_for_tests" / "Patryk, fortnite,naruto.png"


@pytest.mark.full_integration
class TestInitializationUrlUploadFile:
    def test_init01_presigned_put_url_uploads_real_file_to_s3(self, db_session: Session):
        user = create_test_user(db_session)
        image_bytes = IMAGE_PATH.read_bytes()

        result, error, ok = initialization_url_upload_file(
            user_id=str(user.id),
            name=f"test_{uuid.uuid4().hex[:8]}.png",
            original_name="naruto.png",
            size=len(image_bytes),
            file_type=FileType.PHOTO,
            mime_type="image/png",
            catalog="tests",
            db_session=db_session,
        )

        assert ok is True and error is None

        file_record = db_session.get(File, result.file_id)
        s3_key = file_record.s3_key

        try:
            put_response = requests.put(
                result.signed_url,
                data=image_bytes,
                headers={
                    "Content-Type": "image/png",
                    "x-amz-server-side-encryption": "aws:kms",
                    "x-amz-server-side-encryption-aws-kms-key-id": result.kms_key_id,
                },
                timeout=30,
            )
            assert put_response.status_code == 200

            s3_client = get_s3_client()
            head = s3_client.head_object(Bucket=settings.s3_bucket_name, Key=s3_key)
            assert head["ContentLength"] == len(image_bytes)
        finally:
            # sprzątanie — obiekt wylądował na realnym S3, musi zniknąć niezależnie od wyniku asercji
            delete_file_s3(s3_key)
