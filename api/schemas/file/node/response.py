from datetime import datetime

from pydantic import BaseModel


class FilesNodeResponseData(BaseModel):
    id: str
    name: str
    parent_id: str | None
    description: str | None
    is_active: bool
    created_at: datetime | None
    updated_at: datetime | None
