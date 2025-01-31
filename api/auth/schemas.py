from pydantic import BaseModel


class UserDataPayload(BaseModel):
    username: str
    password: str

