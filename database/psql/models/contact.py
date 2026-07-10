import uuid

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from database.psql.base import Base


class ContactMessage(Base):
    """Wiadomość z publicznego formularza kontaktowego.

    `application` identyfikuje frontend/backend nadawcy — wartość pochodzi
    z claimu podpisanego tokena kontaktowego (X-Contact-Token), nie z payloadu.
    """

    __tablename__ = "contact_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=True)
    phone_number = Column(String(30), nullable=False)
    email = Column(String(255), nullable=True)
    description = Column(String, nullable=False)
    application = Column(String(100), nullable=False, index=True)
    status = Column(String, nullable=False, default="new")  # new | read | closed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
