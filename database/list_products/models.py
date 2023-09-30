from sqlalchemy import Column, String, Integer, Boolean
import uuid
from database.db import Base


class ListProducts(Base):
    __tablename__ = "listproducts"

    id = Column(String, primary_key=True, default=uuid.uuid4)
    name = Column(String)
    amount = Column(Integer)
    model = Column(String)
    type = Column(Boolean)

    class Config:
        orm_mode: True
