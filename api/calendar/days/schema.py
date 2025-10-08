from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, Any


class PayloadCalendarDaysWorkUpdate(BaseModel):
    year: int
    month: int
    start_day: int
    end_day: int
    norm_hours: float
    hours_worked: float
    hourly_rate: float


class PayloadCalendarDayWorkUpdateById(BaseModel):
    norm_hours: float
    hours_worked: float
    hourly_rate: float


class PayloadCalendarDaysWorkSalaryUpdate(BaseModel):
    year: int
    month: int
    salary: float
