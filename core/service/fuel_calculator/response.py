from dataclasses import dataclass


@dataclass
class FuelCalculationResponse:
    price: float
    pattern: str
