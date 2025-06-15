from sqlalchemy import Column, String, Boolean, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from database.db import Base


class Tasks(Base):
    __tablename__ = 'tasks'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(String(255), nullable=False)
    time = Column(Integer, nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
