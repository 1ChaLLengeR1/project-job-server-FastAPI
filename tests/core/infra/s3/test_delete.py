import uuid

import pytest
from botocore.exceptions import ClientError

from config.settings import settings
from core.infra.s3.config import get_s3_client
from core.infra.s3.delete import delete_file_s3


@pytest.mark.full_integration
class TestDeleteFileS3:
    def test_delete01_removes_previously_uploaded_object(self):
        s3_client = get_s3_client()
        s3_key = f"tests/{uuid.uuid4().hex}.txt"
        s3_client.put_object(
            Bucket=settings.s3_bucket_name, Key=s3_key, Body=b"smieci-testowe", ContentType="text/plain"
        )

        try:
            result, error, ok = delete_file_s3(s3_key)

            assert ok is True and error is None

            with pytest.raises(ClientError) as exc_info:
                s3_client.head_object(Bucket=settings.s3_bucket_name, Key=s3_key)
            assert exc_info.value.response["Error"]["Code"] == "404"
        finally:
            # bezpiecznik — gdyby delete_file_s3 nie usunął obiektu, awaryjnie sprzątamy sami
            s3_client.delete_object(Bucket=settings.s3_bucket_name, Key=s3_key)

    def test_delete02_returns_not_found_for_missing_key(self):
        missing_key = f"tests/{uuid.uuid4().hex}-nieistniejacy.txt"

        result, error, ok = delete_file_s3(missing_key)

        assert ok is False and result is None
        assert error.key_type_error == "NotFound"
