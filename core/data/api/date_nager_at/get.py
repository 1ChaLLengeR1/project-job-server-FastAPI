from dataclasses import dataclass, asdict
from typing import List, Optional
from datetime import date


@dataclass
class Holiday:
    date: str
    local_name: str
    name: str
    country_code: str
    fixed: bool
    global_: bool
    counties: Optional[List[str]]
    launch_year: Optional[int]
    types: List[str]

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'Holiday':
        return cls(
            date=data["date"],
            local_name=data["localName"],
            name=data["name"],
            country_code=data["countryCode"],
            fixed=data["fixed"],
            global_=data["global"],
            counties=data["counties"],
            launch_year=data["launchYear"],
            types=data["types"]
        )

    @property
    def data_object(self) -> date:
        year, month, day = map(int, self.date.split('-'))
        return date(year, month, day)
