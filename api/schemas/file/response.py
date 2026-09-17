from datetime import date, datetime

from pydantic import BaseModel

from database.psql.models.file import FileStatus, FileType


class FileResponseData(BaseModel):
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


class FileInitResponseData(BaseModel):
    file_id: str
    signed_url: str
    url: str


class FileDeleteResponseData(BaseModel):
    file_id: str


class FileCollectionPaginationData(BaseModel):
    has_more: bool
    page: int
    limit: int
    offset: int
    total: int


class FileCollectionResponseData(BaseModel):
    data: list[FileResponseData]
    pagination: FileCollectionPaginationData


class FileWithChildrenResponseData(BaseModel):
    file: FileResponseData
    children: list[FileResponseData]
