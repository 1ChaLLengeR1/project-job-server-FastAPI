from pydantic import BaseModel


class LoginUserSchema(BaseModel):
    username: str or None = None
    password: str or None = None

    class Config:
        orm_mode: True


class RefreshTokenSchema(BaseModel):
    id: str or None = None
    refresh_token: str or None = None

    class Config:
        orm_mode: True
