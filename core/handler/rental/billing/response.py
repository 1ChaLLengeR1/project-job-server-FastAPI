from dataclasses import dataclass, field

from core.repository.psql.rental.billing.response import BillingPeriodResponse
from core.service.rental.billing.response import ApartmentSettlementResponse
from core.service.rental.family.response import BeneficiaryAllocationItemResponse
from core.service.rental.meters.response import MainMeterErrorResponse, MeterConsumptionResponse


@dataclass
class PeriodAdjustmentInput:
    """Korekta jednorazowa dla mieszkania w okresie (np. "zaległe media" +260, "nadpłata" -19)."""

    apartment_id: str
    name: str
    amount: float  # może być ujemna


@dataclass
class PeriodSettlementPreview:
    apartment_id: str
    apartment_name: str
    settlement: ApartmentSettlementResponse


@dataclass
class PeriodBeneficiaryPreview:
    beneficiary_id: str
    beneficiary_name: str
    total_amount: float
    items: list[BeneficiaryAllocationItemResponse] = field(default_factory=list)


@dataclass
class PeriodPreviewResponse:
    """Pełne wyliczenie okresu (na żywo) — odpowiednik jednego pliku Obliczenia*.txt."""

    period: BillingPeriodResponse
    electricity_rate: float  # zł/kWh użyta w wyliczeniu (z rachunku lub ręczna)
    electricity_total_consumption: float  # suma kWh liczników mieszkań
    main_meter_error: MainMeterErrorResponse | None  # None = brak odczytu licznika głównego
    consumptions: list[MeterConsumptionResponse] = field(default_factory=list)
    settlements: list[PeriodSettlementPreview] = field(default_factory=list)
    beneficiaries: list[PeriodBeneficiaryPreview] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
