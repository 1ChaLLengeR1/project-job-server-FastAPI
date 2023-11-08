from sqlalchemy import Column, String, Float, Integer
import uuid
from database.db import Base


class Renting(Base):
    __tablename__ = "renting_user"

    id = Column(String, primary_key=True, default=uuid.uuid4)
    name = Column(String)
    quantity_users = Column(Integer)
    name_flats = Column(String)
    id_flats = Column(String)

    class Config:
        orm_mode: True