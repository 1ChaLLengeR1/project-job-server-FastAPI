import enum
import uuid

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from database.psql.base import Base


class FileStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CONFIRMED = "confirmed"


class FileType(str, enum.Enum):
    PHOTO = "photo"
    VIDEO = "video"
    GIF = "gif"
    AUDIO = "audio"


class File(Base):
    __tablename__ = "files"
    __table_args__ = (
        Index("ix_files_status", "status"),
        Index("ix_files_file_type", "file_type"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=True, index=True)

    original_name = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    size = Column(BigInteger, nullable=False)
    file_type = Column(Enum(FileType, name="file_type"), nullable=False)
    mime_type = Column(String(255), nullable=True)
    s3_key = Column(String(512), nullable=False, unique=True)
    s3_prefix = Column(String(512), nullable=False)
    url = Column(String(512), nullable=True)

    status = Column(Enum(FileStatus, name="file_status"), nullable=False, default=FileStatus.PENDING)

    # S3 multipart upload tracking (dla dużych plików video/audio)
    multipart_upload_id = Column(String(1024), nullable=True)
    chunk_size = Column(Integer, nullable=True)
    total_chunks = Column(Integer, nullable=True)
    uploaded_chunks = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
