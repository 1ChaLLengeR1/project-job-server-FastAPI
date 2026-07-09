from pydantic import BaseModel, Field


class FuelCalculationPayload(BaseModel):
    way: float = Field(ge=0, description="Dystans w kilometrach")
    fuel: float = Field(ge=0, description="Cena paliwa za litr")
    combustion: float = Field(ge=0, description="Spalanie na 100 km")
    remaining_values: float = Field(description="Dodatkowe koszty doliczane do wyniku")
