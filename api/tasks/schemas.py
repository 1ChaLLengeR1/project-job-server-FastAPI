from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel


class PayloadTaskCreate(BaseModel):
    description: str
    time: int
    active: bool


class PayloadTaskUpdate(BaseModel):
    description: str | None = None
    time: Any | None = None


class PayloadTaskUpdateActive(BaseModel):
    active: bool


class ResponseSerializerTask(BaseModel):
    id: UUID
    description: str
    time: int
    active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {UUID: lambda u: str(u), datetime: lambda dt: dt.isoformat()}
