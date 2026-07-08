import uuid

from sqlalchemy import Column, Date, String
from sqlalchemy.dialects.postgresql import UUID

from database.psql.base import Base


class Logs(Base):
    __tablename__ = "logs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String)
    description = Column(String)
    date = Column(Date)

    class Config:
        orm_mode = True
