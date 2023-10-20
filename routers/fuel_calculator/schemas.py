from pydantic import BaseModel


class FuelParams(BaseModel):
    way: float | str
    fuel: float | str
    combustion: float | str
    remaining_values: float | str

    class Config:
        orm_mode = True