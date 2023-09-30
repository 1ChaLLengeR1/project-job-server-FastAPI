from pydantic import BaseModel


class FuelParams(BaseModel):
    way: float
    fuel: float
    combustion: float
    remaining_values: float

    class Config:
        orm_mode = True