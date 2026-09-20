import enum
import uuid

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
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
    DOCUMENT = "document"


class FilesNode(Base):
    """Drzewo podmiotów (osoba lub kategoria - ten sam byt), po którym rozpina się pliki."""

    __tablename__ = "files_nodes"
    __table_args__ = (UniqueConstraint("parent_id", "name", name="uq_files_nodes_parent_name"),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    parent_id = Column(
        UUID(as_uuid=True), ForeignKey("files_nodes.id", ondelete="RESTRICT"), nullable=True, index=True
    )
    description = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class File(Base):
    __tablename__ = "files"
    __table_args__ = (
        Index("ix_files_status", "status"),
        Index("ix_files_file_type", "file_type"),
        # confirmed = przypisany do wezla (zob. PLAN_MAGAZYN_PLIKOW.md, sekcja 3.2)
        CheckConstraint(
            "status != 'CONFIRMED' OR node_id IS NOT NULL", name="ck_files_confirmed_requires_node"
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=True, index=True)
    # NULL dopoki plik nie jest podpiety do wezla (patrz status pliku w PLAN_MAGAZYN_PLIKOW.md)
    node_id = Column(
        UUID(as_uuid=True), ForeignKey("files_nodes.id", ondelete="RESTRICT"), nullable=True, index=True
    )
    # plik-dziecko (np. "faktura" -> "faktura-1-2"), niezalezne od node_id;
    # jedyne miejsce z CASCADE - dziecko nie ma sensu bez rodzica
    parent_file_id = Column(UUID(as_uuid=True), ForeignKey("files.id", ondelete="CASCADE"), nullable=True, index=True)

    original_name = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    size = Column(BigInteger, nullable=False)
    file_type = Column(Enum(FileType, name="file_type"), nullable=False)
    mime_type = Column(String(255), nullable=True)
    s3_key = Column(String(512), nullable=False, unique=True)
    s3_prefix = Column(String(512), nullable=False)
    url = Column(String(512), nullable=True)

    status = Column(Enum(FileStatus, name="file_status"), nullable=False, default=FileStatus.PENDING)

    description = Column(String, nullable=True)
    guarantee_start_date = Column(Date, nullable=True)
    guarantee_end_date = Column(Date, nullable=True)

    # S3 multipart upload tracking (dla dużych plików video/audio)
    multipart_upload_id = Column(String(1024), nullable=True)
    chunk_size = Column(Integer, nullable=True)
    total_chunks = Column(Integer, nullable=True)
    uploaded_chunks = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
