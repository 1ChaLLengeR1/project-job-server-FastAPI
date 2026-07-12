from pydantic import BaseModel


class FuelCalculationResponseData(BaseModel):
    price: float
    pattern: str
