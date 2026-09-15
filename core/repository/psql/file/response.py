from dataclasses import dataclass
from datetime import datetime

from database.psql.models.file import File, FileStatus, FileType


@dataclass
class FileResponse:
    id: str
    user_id: str | None
    name: str
    original_name: str
    size: int
    file_type: FileType
    mime_type: str | None
    s3_key: str
    s3_prefix: str
    url: str | None
    status: FileStatus
    created_at: datetime | None
    updated_at: datetime | None


def _to_file_response(model: File) -> FileResponse:
    return FileResponse(
        id=str(model.id),
        user_id=str(model.user_id) if model.user_id else None,
        name=model.name,
        original_name=model.original_name,
        size=model.size,
        file_type=model.file_type,
        mime_type=model.mime_type,
        s3_key=model.s3_key,
        s3_prefix=model.s3_prefix,
        url=model.url,
        status=model.status,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


@dataclass
class RepositoryDeleteFileResponse:
    id: str
    s3_key: str


def _to_delete_file_response(model: File) -> RepositoryDeleteFileResponse:
    return RepositoryDeleteFileResponse(id=str(model.id), s3_key=model.s3_key)


@dataclass
class RepositoryCollectionFilePagination:
    has_more: bool
    page: int
    limit: int
    offset: int
    total: int


@dataclass
class RepositoryCollectionFileResponse:
    data: list[FileResponse]
    pagination: RepositoryCollectionFilePagination
