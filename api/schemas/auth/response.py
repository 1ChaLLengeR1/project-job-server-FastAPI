from pydantic import BaseModel


class AuthTokensData(BaseModel):
    id: str
    username: str
    access_token: str
    refresh_token: str
