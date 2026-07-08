from typing import TypedDict


class CalculatorData(TypedDict, total=False):
    gross_sales: float
    gross_purchase: float
    provision: float
    distinction: float
    referrer: str
