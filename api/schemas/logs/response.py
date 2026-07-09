from datetime import date

from pydantic import BaseModel


class LogResponseData(BaseModel):
    id: str
    username: str
    description: str
    date: date | None
