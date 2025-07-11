from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from database.db import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String)
    password = Column(String)
    type = Column(String)

    class Config:
        orm_mode = True
