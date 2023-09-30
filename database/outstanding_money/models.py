from sqlalchemy import Column, String, Float, Date
import uuid
from database.db import Base


class NamesOverdue(Base):
    __tablename__ = 'namesoverdue'

    id = Column(String, primary_key=True, default=uuid.uuid4)
    name = Column(String)

    class Config:
        orm_mode = True


class OutStandingMoney(Base):
    __tablename__ = 'outstandingmoney'

    id = Column(String, primary_key=True, default=uuid.uuid4)
    amount = Column(Float)
    name = Column(String)
    date = Column(Date)
    id_name = Column(String)

    class Config:
        orm_mode = True
