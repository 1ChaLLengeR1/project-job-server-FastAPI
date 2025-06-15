from pydantic import BaseModel


class PayloadTaskCreate(BaseModel):
    description: str
    time: int
    active: bool