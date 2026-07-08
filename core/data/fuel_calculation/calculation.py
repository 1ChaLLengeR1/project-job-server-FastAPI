from typing import TypedDict


class FuelData(TypedDict, total=False):
    way: float
    fuel: float
    combustion: float
    remaining_values: float
