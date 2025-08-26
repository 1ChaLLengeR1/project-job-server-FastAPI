from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, Any


class PayloadCalendarConditionCreate(BaseModel):
    norm_hours: Any
    hourly_rate: Any