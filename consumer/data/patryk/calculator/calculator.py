from typing import TypedDict, Union, Dict, Any, List, Literal, Optional


class CalculatorData(TypedDict, total=False):
    gross_sales: float
    gross_purchase: float
    provision: float
    distinction: float
    referrer: str
