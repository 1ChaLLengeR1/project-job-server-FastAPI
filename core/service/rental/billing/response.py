from dataclasses import dataclass, field


@dataclass
class ApartmentCostInput:
    """Koszt stały przypisany do mieszkania — wejście do wyceny pozycji rozliczenia."""

    cost_type_id: str
    name: str  # np. "śmieci", "internet", "garaż"
    charge_type: str  # fixed | per_person
    amount: float  # dla per_person: stawka za osobę


@dataclass
class AdjustmentInput:
    """Korekta jednorazowa (np. "zaległe media" +260, "nadpłata" -19)."""

    name: str
    amount: float  # może być ujemna


@dataclass
class MediaCostResponse:
    consumption: float
    rate: float
    cost: float  # zaokrąglone do pełnych złotych (half-up, jak "~" w notatkach)


@dataclass
class SettlementItemCalcResponse:
    name: str
    kind: str  # fixed_cost | adjustment
    amount: float
    cost_type_id: str | None = None


@dataclass
class ApartmentSettlementResponse:
    apartment_id: str
    tenancy_id: str | None
    rent_amount: float
    electricity_consumption: float
    electricity_cost: float
    water_consumption: float
    water_cost: float
    total_media_amount: float  # media + koszty stałe + korekty ("Razem" z notatek, bez czynszu)
    total_amount: float  # total_media_amount + rent_amount
    items: list[SettlementItemCalcResponse] = field(default_factory=list)
