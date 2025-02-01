from typing import TypedDict, Union, Dict, Any, List, Literal, Optional


class KeysCalculatorData(TypedDict, total=False):
    id: str
    income_tax: float
    vat: float
    inpost_parcel_locker: float
    inpost_courier: float
    inpost_cash_of_delivery_courier: float
    dpd: float
    allegro_matt: float
    without_smart: float
