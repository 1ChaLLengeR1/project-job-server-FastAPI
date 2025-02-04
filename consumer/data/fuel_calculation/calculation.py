from typing import TypedDict, Union, Dict, Any, List, Literal, Optional


class FuelData(TypedDict, total=False):
    way: float
    fuel: float
    combustion: float
    remaining_values: float
