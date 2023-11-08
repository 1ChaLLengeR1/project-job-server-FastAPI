from sqlalchemy import Column, String
import uuid
from database.db import Base

class ListProducts(Base):
    __tablename__ = "flats"

    id = Column(String, primary_key=True, default=uuid.uuid4)
    house_name = Column(String)
    professional_house_name = Column(String)

    class Config:
        orm_mode: True