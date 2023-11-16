from sqlalchemy import Column, String, Double
import uuid
from database.db import Base

class BasicRentalValues(Base):
    __tablename__ = "basic_rental_values"

    id = Column(String, primary_key=True, default=uuid.uuid4)
    electric_current = Column(Double)
    water = Column(Double)
    transfer = Column(Double)
    trash = Column(Double)
    internet = Column(Double)
    

    class Config:
        orm_mode: True