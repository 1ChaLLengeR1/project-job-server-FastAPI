from sqlalchemy import Column, String, Integer
import uuid
from database.db import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=uuid.uuid4)
    username = Column(String)
    password = Column(String)
    type = Column(String)

    class Config:
        orm_mode = True
