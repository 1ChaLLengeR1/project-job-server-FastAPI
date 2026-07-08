from typing import Any

from pydantic import BaseModel


class PayloadCalendarConditionCreate(BaseModel):
    norm_hours: Any
    hourly_rate: Any
