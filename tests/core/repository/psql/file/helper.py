from datetime import date
from uuid import uuid4

from sqlalchemy.orm import Session

from database.psql.models.file import File, FileStatus, FileType


def make_file(
    db: Session,
    *,
    name: str | None = None,
    original_name: str | None = None,
    size: int = 1024,
    file_type: FileType = FileType.PHOTO,
    mime_type: str = "image/png",
    status: FileStatus = FileStatus.PENDING,
    user_id: str | None = None,
    node_id: str | None = None,
    parent_file_id: str | None = None,
    description: str | None = None,
    guarantee_start_date: date | None = None,
    guarantee_end_date: date | None = None,
) -> File:
    unique_name = name or f"file_{uuid4().hex[:8]}.png"
    file = File(
        user_id=user_id,
        node_id=node_id,
        parent_file_id=parent_file_id,
        name=unique_name,
        original_name=original_name or unique_name,
        size=size,
        file_type=file_type,
        mime_type=mime_type,
        s3_key=f"tests/{uuid4().hex}_{unique_name}",
        s3_prefix="tests",
        status=status,
        description=description,
        guarantee_start_date=guarantee_start_date,
        guarantee_end_date=guarantee_end_date,
    )
    db.add(file)
    db.flush()
    return file
