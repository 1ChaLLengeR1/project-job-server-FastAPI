import uuid

import pytest
import requests

from config.settings import settings
from core.infra.s3.config import get_s3_client
from core.infra.s3.get import generate_get_presigned_url


@pytest.mark.full_integration
class TestGenerateGetPresignedUrl:
    def test_get01_presigned_url_downloads_real_object_with_content_disposition(self):
        s3_client = get_s3_client()
        s3_key = f"tests/{uuid.uuid4().hex}.txt"
        content = b"zawartosc testowego pliku"
        s3_client.put_object(Bucket=settings.s3_bucket_name, Key=s3_key, Body=content, ContentType="text/plain")

        try:
            signed_url, error, ok = generate_get_presigned_url(
                s3_key=s3_key, expires_seconds=60, disposition="attachment", filename="pobrany.txt"
            )

            assert ok is True and error is None

            response = requests.get(signed_url, timeout=30)
            assert response.status_code == 200
            assert response.content == content
            assert response.headers["Content-Disposition"] == (
                "attachment; filename=\"pobrany.txt\"; filename*=UTF-8''pobrany.txt"
            )
        finally:
            s3_client.delete_object(Bucket=settings.s3_bucket_name, Key=s3_key)

    def test_get02_non_ascii_filename_does_not_break_s3_signature(self):
        """Regresja: polskie znaki w filename ('Ś' itp.) nie mieszcza sie w
        ISO-8859-1, ktorego wymaga naglowek ResponseContentDisposition - bez
        RFC 6266 encodingu (filename*=UTF-8''...) S3 zwracal InvalidArgument."""
        s3_client = get_s3_client()
        s3_key = f"tests/{uuid.uuid4().hex}.txt"
        content = b"zawartosc testowego pliku"
        s3_client.put_object(Bucket=settings.s3_bucket_name, Key=s3_key, Body=content, ContentType="text/plain")

        try:
            signed_url, error, ok = generate_get_presigned_url(
                s3_key=s3_key, expires_seconds=60, disposition="inline", filename="CV_ArturŚcibor_EN.pdf"
            )

            assert ok is True and error is None

            response = requests.get(signed_url, timeout=30)
            assert response.status_code == 200
            assert response.content == content
            assert "filename*=UTF-8''CV_Artur%C5%9Acibor_EN.pdf" in response.headers["Content-Disposition"]
        finally:
            s3_client.delete_object(Bucket=settings.s3_bucket_name, Key=s3_key)
