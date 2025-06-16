from pydantic import BaseModel


class PayloadTaskCreate(BaseModel):
    description: str
    time: int
    active: bool


class PayloadTaskUpdate(BaseModel):
    description: str


class PayloadTaskUpdateActive(BaseModel):
    active: bool
