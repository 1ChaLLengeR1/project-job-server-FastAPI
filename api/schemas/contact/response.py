from datetime import datetime

from pydantic import BaseModel


class ContactMessageResponseData(BaseModel):
    id: str
    first_name: str
    last_name: str | None
    phone_number: str
    email: str | None
    description: str
    application: str
    status: str
    created_at: datetime | None
    updated_at: datetime | None
