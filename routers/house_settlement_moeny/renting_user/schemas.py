from pydantic import BaseModel


class RentingUser(BaseModel):
    id: str | None = None
    id_user: str | None = None
    username: str | None = None
    name: str | None = None
    quantity_users: int | None = None
    name_flats: str | None = None
    id_flats: str | None = None

    class Config:
        orm_mode: True