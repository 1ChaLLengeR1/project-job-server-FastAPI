from datetime import datetime

from pydantic import BaseModel


class LogResponseData(BaseModel):
    id: str
    username: str
    description: str
    date: datetime | None
