from sqlalchemy import Column, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid
from database.db import Base


class KeysCalculatorPatryk(Base):
    __tablename__ = "keyscalculatorpatryk"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    income_tax = Column(Float)
    vat = Column(Float)
    inpost_parcel_locker = Column(Float)
    inpost_courier = Column(Float)
    inpost_cash_of_delivery_courier = Column(Float)
    dpd = Column(Float)
    allegro_matt = Column(Float)
    without_smart = Column(Float)

    class Config:
        orm_mode = True
