from sqlalchemy import Column, Integer, Float, Boolean, Date, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from database.db import Base


class WorkDay(Base):
    __tablename__ = "calendar_work_days"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    date = Column(Date, unique=True, nullable=False)
    hours_worked = Column(Float, nullable=True)
    is_holiday = Column(Boolean, default=False, nullable=False)
    norm_hours = Column(Float, nullable=False)
    hourly_rate = Column(Float, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class WorkConditionChange(Base):
    __tablename__ = "calendar_work_condition_changes"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    start_date = Column(Date, nullable=False)
    norm_hours = Column(Float, nullable=False)
    hourly_rate = Column(Float, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
