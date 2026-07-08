from typing import Any

from pydantic import BaseModel


class PayloadCalendarCreate(BaseModel):
    year: Any
