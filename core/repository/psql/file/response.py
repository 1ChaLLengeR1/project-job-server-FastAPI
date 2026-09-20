from dataclasses import dataclass
from datetime import date, datetime

from database.psql.models.file import File, FileStatus, FileType


@dataclass
class FileResponse:
    id: str
    user_id: str | None
    node_id: str | None
    parent_file_id: str | None
    name: str
    original_name: str
    size: int
    file_type: FileType
    mime_type: str | None
    s3_key: str
    s3_prefix: str
    url: str | None
    status: FileStatus
    description: str | None
    guarantee_start_date: date | None
    guarantee_end_date: date | None
    created_at: datetime | None
    updated_at: datetime | None


def _to_file_response(model: File) -> FileResponse:
    return FileResponse(
        id=str(model.id),
        user_id=str(model.user_id) if model.user_id else None,
        node_id=str(model.node_id) if model.node_id else None,
        parent_file_id=str(model.parent_file_id) if model.parent_file_id else None,
        name=model.name,
        original_name=model.original_name,
        size=model.size,
        file_type=model.file_type,
        mime_type=model.mime_type,
        s3_key=model.s3_key,
        s3_prefix=model.s3_prefix,
        url=model.url,
        status=model.status,
        description=model.description,
        guarantee_start_date=model.guarantee_start_date,
        guarantee_end_date=model.guarantee_end_date,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


@dataclass
class RepositoryDeleteFileResponse:
    id: str
    s3_key: str
    child_s3_keys: list[str]


def _to_delete_file_response(model: File, child_s3_keys: list[str] | None = None) -> RepositoryDeleteFileResponse:
    return RepositoryDeleteFileResponse(id=str(model.id), s3_key=model.s3_key, child_s3_keys=child_s3_keys or [])


@dataclass
class FileWithChildrenResponse:
    file: FileResponse
    children: list[FileResponse]


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
