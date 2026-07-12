from dataclasses import dataclass, field


@dataclass
class MeterReadingInput:
    """Odczyt licznika wraz z danymi licznika — wejście do obliczeń zużycia."""

    meter_id: str
    apartment_id: str | None  # None = licznik główny budynku
    media_type: str  # electricity | water
    is_master: bool
    previous_value: float  # "Ostatnio"
    current_value: float  # "Teraz"
    error_correction: float = 0.0  # "Błąd_Licznika"


@dataclass
class MeterConsumptionResponse:
    meter_id: str
    apartment_id: str | None
    media_type: str
    raw_difference: float  # current - previous
    consumption: float  # po odjęciu podliczników (master) i korekcie błędu
    error_correction: float
    is_master: bool


@dataclass
class MeterErrorProposalResponse:
    meter_id: str
    apartment_id: str | None
    proposed_correction: float


@dataclass
class MainMeterErrorResponse:
    main_difference: float  # różnica licznika głównego
    apartments_total: float  # suma zużyć liczników mieszkań
    error: float  # main_difference - apartments_total ("Błąd_między_licznikami")
    proposals: list[MeterErrorProposalResponse] = field(default_factory=list)


@dataclass
class ElectricityRateResponse:
    bill_amount: float  # kwota rachunku globalnego ("Do zapłaty")
    total_consumption: float  # suma kWh
    rate: float  # zł/kWh, 4 miejsca po przecinku
