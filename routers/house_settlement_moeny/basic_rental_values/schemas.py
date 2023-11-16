from pydantic import BaseModel


class BasicRental(BaseModel):
    id: str | None = None
    id_user: str | None = None
    username: str | None = None
    electric_current: float | None = None
    water: float | None = None
    transfer: float | None = None
    trash: float | None = None
    internet: float | None = None

    class Config:
        orm_mode: True