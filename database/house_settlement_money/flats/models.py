from sqlalchemy import Column, String, Float
import uuid
from database.db import Base

class Flats(Base):
    __tablename__ = "flats"

    id = Column(String, primary_key=True, default=uuid.uuid4)
    house_name = Column(String)
    professional_house_name = Column(String)
    price = Column(Float, default=0)

    class Config:
        orm_mode: True