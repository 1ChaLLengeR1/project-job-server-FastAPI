from pydantic import BaseModel


class FlatsParams(BaseModel):
    id: str | None = None
    id_user: str | None = None
    username: str | None = None
    house_name: str | None = None
    professional_house_name: str | None = None
    price: float | None = None

    class Config:
        orm_mode: True
