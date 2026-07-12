from api.response import ApiErrorData
from core.service.rental.meters.response import (
    ElectricityRateResponse,
    MainMeterErrorResponse,
    MeterConsumptionResponse,
    MeterErrorProposalResponse,
    MeterReadingInput,
)


def calculation_meter_consumptions(
    readings: list[MeterReadingInput],
) -> tuple[list[MeterConsumptionResponse] | None, ApiErrorData | None, bool]:
    """Zużycie per licznik: różnica odczytów + korekta błędu.

    Licznik z is_master=True (nadrzędny) obejmuje pozostałe liczniki mieszkań tego samego
    medium — jego zużycie = własna różnica - suma różnic pozostałych liczników mieszkań
    (przypadek wody Pokoju Łukasza z ręcznych obliczeń).
    """
    try:
        raw_differences: dict[str, float] = {}
        for reading in readings:
            raw = round(reading.current_value - reading.previous_value, 3)
            if raw < 0:
                return (
                    None,
                    ApiErrorData(
                        message=(
                            f"Odczyt 'Teraz' ({reading.current_value}) mniejszy niż 'Ostatnio' "
                            f"({reading.previous_value}) dla licznika {reading.meter_id}"
                        ),
                        type_module="calculation_meter_consumptions",
                        type_error="exception",
                        key_type_error="Exception",
                    ),
                    False,
                )
            raw_differences[reading.meter_id] = raw

        masters_per_media: dict[str, int] = {}
        for reading in readings:
            if reading.is_master and reading.apartment_id is not None:
                masters_per_media[reading.media_type] = masters_per_media.get(reading.media_type, 0) + 1
        for media_type, masters_count in masters_per_media.items():
            if masters_count > 1:
                return (
                    None,
                    ApiErrorData(
                        message=f"Więcej niż jeden licznik nadrzędny dla medium '{media_type}'",
                        type_module="calculation_meter_consumptions",
                        type_error="exception",
                        key_type_error="Exception",
                    ),
                    False,
                )

        results = []
        for reading in readings:
            raw = raw_differences[reading.meter_id]

            if reading.apartment_id is None:
                # licznik główny budynku — zużycie informacyjne, bez korekt
                consumption = raw
            elif reading.is_master:
                others_total = sum(
                    raw_differences[other.meter_id]
                    for other in readings
                    if other.meter_id != reading.meter_id
                    and other.apartment_id is not None
                    and other.media_type == reading.media_type
                )
                consumption = round(raw - others_total + reading.error_correction, 3)
                if consumption < 0:
                    return (
                        None,
                        ApiErrorData(
                            message=(
                                f"Ujemne zużycie licznika nadrzędnego {reading.meter_id}: "
                                f"różnica {raw} minus podliczniki {round(others_total, 3)}"
                            ),
                            type_module="calculation_meter_consumptions",
                            type_error="exception",
                            key_type_error="Exception",
                        ),
                        False,
                    )
            else:
                consumption = round(raw + reading.error_correction, 3)

            results.append(
                MeterConsumptionResponse(
                    meter_id=reading.meter_id,
                    apartment_id=reading.apartment_id,
                    media_type=reading.media_type,
                    raw_difference=raw,
                    consumption=consumption,
                    error_correction=reading.error_correction,
                    is_master=reading.is_master,
                )
            )
        return results, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="calculation_meter_consumptions",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def calculation_main_meter_error(
    main_difference: float,
    apartment_consumptions: list[MeterConsumptionResponse],
) -> tuple[MainMeterErrorResponse | None, ApiErrorData | None, bool]:
    """Błąd między licznikiem głównym a sumą liczników mieszkań ("Błąd_między_licznikami").

    Propozycja korekty: równy podział błędu na liczniki mieszkań ze zużyciem > 0
    (jak +4 kWh per mieszkanie w ręcznych obliczeniach) — edytowalna przed zamknięciem okresu.
    """
    try:
        if main_difference < 0:
            return (
                None,
                ApiErrorData(
                    message=f"Ujemna różnica licznika głównego: {main_difference}",
                    type_module="calculation_main_meter_error",
                    type_error="exception",
                    key_type_error="Exception",
                ),
                False,
            )

        apartments_total = round(sum(consumption.consumption for consumption in apartment_consumptions), 3)
        error = round(main_difference - apartments_total, 3)

        consuming = [consumption for consumption in apartment_consumptions if consumption.consumption > 0]
        proposals = []
        if consuming and error != 0:
            per_meter = round(error / len(consuming), 3)
            proposals = [
                MeterErrorProposalResponse(
                    meter_id=consumption.meter_id,
                    apartment_id=consumption.apartment_id,
                    proposed_correction=per_meter,
                )
                for consumption in consuming
            ]

        return (
            MainMeterErrorResponse(
                main_difference=main_difference,
                apartments_total=apartments_total,
                error=error,
                proposals=proposals,
            ),
            None,
            True,
        )
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="calculation_main_meter_error",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def calculation_electricity_rate(
    bill_amount: float, total_consumption: float
) -> tuple[ElectricityRateResponse | None, ApiErrorData | None, bool]:
    """Stawka zł/kWh z rachunku globalnego: kwota / suma kWh (jak 899,48 / 855,73 = 1,05)."""
    try:
        if bill_amount < 0:
            return (
                None,
                ApiErrorData(
                    message=f"Ujemna kwota rachunku: {bill_amount}",
                    type_module="calculation_electricity_rate",
                    type_error="exception",
                    key_type_error="Exception",
                ),
                False,
            )
        if total_consumption <= 0:
            return (
                None,
                ApiErrorData(
                    message=f"Suma zużycia musi być większa od zera, otrzymano: {total_consumption}",
                    type_module="calculation_electricity_rate",
                    type_error="exception",
                    key_type_error="Exception",
                ),
                False,
            )

        rate = round(bill_amount / total_consumption, 4)
        return (
            ElectricityRateResponse(
                bill_amount=bill_amount,
                total_consumption=total_consumption,
                rate=rate,
            ),
            None,
            True,
        )
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="calculation_electricity_rate",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
