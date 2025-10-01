from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, Any


class PayloadCalendarCreate(BaseModel):
    year: Any
