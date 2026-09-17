from dataclasses import dataclass


@dataclass
class S3InitUploadFileResponse:
    file_id: str
    signed_url: str
    url: str | None
