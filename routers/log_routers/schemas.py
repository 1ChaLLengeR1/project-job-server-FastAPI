from pydantic import BaseModel


class Log(BaseModel):
    username: str
    description: str

    class Config:
        orm_mode = True
