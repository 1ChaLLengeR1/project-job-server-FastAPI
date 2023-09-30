from sqlalchemy import Column, String, Date
import uuid
from database.db import Base


class Logs(Base):
    __tablename__ = 'logs'
    id = Column(String, primary_key=True, default=uuid.uuid4)
    username = Column(String)
    description = Column(String)
    date = Column(Date)

    class Config:
        orm_mode = True
