from dataclasses import dataclass


@dataclass
class ServiceDeleteFileResponse:
    file_id: str


@dataclass
class ServiceFileUrlResponse:
    file_id: str
    url: str
    expires_in_seconds: int
