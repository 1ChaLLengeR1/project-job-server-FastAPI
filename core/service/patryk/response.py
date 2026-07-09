from dataclasses import dataclass


@dataclass
class CalculationResponse:
    brutto: float
    na_czysto: float
    zysk_procentowy: float
