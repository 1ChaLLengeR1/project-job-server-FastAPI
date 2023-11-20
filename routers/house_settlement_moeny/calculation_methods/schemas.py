from pydantic import BaseModel


class MainCounters(BaseModel):
    now_meter_electric: float or None = None
    now_meter_water: float or None = None
    lately_meter_electric: float or None = None
    lately_meter_water: float or None = None
    rentals: list = []

    class Config:
        orm_mode: True


