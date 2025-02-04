from pydantic import BaseModel

class FuelData(BaseModel):
    way: float
    fuel: float
    combustion: float
    remaining_values: float