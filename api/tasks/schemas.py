from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, Any


class PayloadTaskCreate(BaseModel):
    description: str
    time: int
    active: bool


class PayloadTaskUpdate(BaseModel):
    description: Optional[str] = None
    time: Optional[Any] = None


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
        json_encoders = {
            UUID: lambda u: str(u),
            datetime: lambda dt: dt.isoformat()
        }
