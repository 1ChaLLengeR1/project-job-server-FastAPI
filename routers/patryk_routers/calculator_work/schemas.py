from pydantic import BaseModel


class CalculatorParams(BaseModel):
    id: str
    username: str
    gross_sales: float
    gross_purchase: float
    provision: float | None = 0
    distinction: float | None = 0
    referrer: str

    class Config:
        orm_mode: True


class KeysCalculator(BaseModel):
    id: str
    id_user: str
    username: str
    income_tax: float
    vat: float
    inpost_parcel_locker: float
    inpost_courier: float
    inpost_cash_of_delivery_courier: float
    dpd: float
    allegro_matt: float
    without_smart: float

    class Config:
        orm_mode: True
