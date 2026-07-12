from dataclasses import dataclass, field


@dataclass
class AllocationRuleInput:
    """Reguła podziału rodzinnego — wejście do rozdzielenia rozliczeń na beneficjentów."""

    rule_id: str
    beneficiary_id: str
    component: str  # rent | electricity | water | cost_type | recurring
    mode: str  # fixed_amount | full
    apartment_id: str | None = None  # None = wszystkie mieszkania / nie dotyczy (recurring)
    cost_type_id: str | None = None  # wymagane dla component=cost_type
    amount: float | None = None  # wymagane dla fixed_amount i recurring; może być ujemna
    description: str | None = None  # etykieta pozycji (np. "podatek", "telefon")


@dataclass
class AllocationSettlementItemInput:
    """Pozycja rozliczenia mieszkania — do dopasowania reguł component=cost_type."""

    name: str
    kind: str  # fixed_cost | adjustment
    amount: float
    cost_type_id: str | None = None


@dataclass
class AllocationSettlementInput:
    """Rozliczenie mieszkania w okresie — wejście do podziału rodzinnego."""

    apartment_id: str
    apartment_name: str
    rent_amount: float
    electricity_cost: float
    water_cost: float
    settlement_id: str | None = None  # id snapshotu (przy preview jeszcze brak)
    items: list[AllocationSettlementItemInput] = field(default_factory=list)


@dataclass
class BeneficiaryAllocationItemResponse:
    description: str  # np. "czynsz - Pokój Łukasza", "prąd - wszystkie mieszkania", "podatek"
    amount: float
    rule_id: str | None = None
    settlement_id: str | None = None


@dataclass
class BeneficiaryAllocationResponse:
    beneficiary_id: str
    total_amount: float
    items: list[BeneficiaryAllocationItemResponse] = field(default_factory=list)


@dataclass
class FamilyAllocationResponse:
    beneficiaries: list[BeneficiaryAllocationResponse] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)  # np. czynsz rozdzielony != czynsz mieszkania
