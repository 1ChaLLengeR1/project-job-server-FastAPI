"""Testy obliczeń liczników na realnych danych z docs/Obliczenia*.txt."""

from core.service.rental.meters.calculation import (
    calculation_electricity_rate,
    calculation_main_meter_error,
    calculation_meter_consumptions,
)
from core.service.rental.meters.response import MeterReadingInput


def _obliczenia3_electricity(error_correction: float = 0) -> list[MeterReadingInput]:
    """Odczyty prądu z Obliczenia_3 (czerwiec: Dudzik, Kydr, Witek, Łukasz + licznik główny)."""
    return [
        MeterReadingInput("el_main", None, "electricity", False, 23132, 23990),
        MeterReadingInput("el_dudzik", "ap_dudzik", "electricity", False, 5621.26, 5938.86, error_correction),
        MeterReadingInput("el_kydr", "ap_kydr", "electricity", False, 5245.77, 5330.12, error_correction),
        MeterReadingInput("el_witek", "ap_witek", "electricity", False, 533.75, 810.93, error_correction),
        MeterReadingInput("el_lukasz", "ap_lukasz", "electricity", False, 3068.36, 3244.96, error_correction),
    ]


class TestCalculationMeterConsumptions:
    def test_consumptions01_obliczenia3_with_error_correction(self):
        # "Błąd_Licznika: 1" — po +1 kWh do każdego mieszkania
        result, err, ok = calculation_meter_consumptions(_obliczenia3_electricity(error_correction=1))

        assert ok is True and err is None
        by_id = {consumption.meter_id: consumption for consumption in result}
        assert by_id["el_dudzik"].consumption == 318.6  # 5938,86 - 5621,26 + 1
        assert by_id["el_kydr"].consumption == 85.35  # 5330,12 - 5245,77 + 1
        assert by_id["el_witek"].consumption == 278.18  # 810,93 - 533,75 + 1
        assert by_id["el_lukasz"].consumption == 177.6  # 3244,96 - 3068,36 + 1
        assert by_id["el_main"].consumption == 858  # licznik główny: 23990 - 23132

    def test_consumptions02_master_water_obliczenia1(self):
        # woda z Obliczenia_1: licznik Łukasza nadrzędny
        readings = [
            MeterReadingInput("w_dudzik", "ap_dudzik", "water", False, 13.479, 19.255),
            MeterReadingInput("w_ania", "ap_ania", "water", False, 65.495, 68.116),
            MeterReadingInput("w_lukasz", "ap_lukasz", "water", True, 205.858, 215.682),
        ]

        result, err, ok = calculation_meter_consumptions(readings)

        assert ok is True
        by_id = {consumption.meter_id: consumption for consumption in result}
        assert by_id["w_dudzik"].consumption == 5.776
        assert by_id["w_ania"].consumption == 2.621
        # 9,824 - 5,776 - 2,621 = 1,427 (dokładnie jak w notatce)
        assert by_id["w_lukasz"].consumption == 1.427
        assert by_id["w_lukasz"].raw_difference == 9.824

    def test_consumptions03_master_electricity_obliczenia1(self):
        # prąd z Obliczenia_1: licznik Łukasza główny dla mieszkań
        readings = [
            MeterReadingInput("el_dudzik", "ap_dudzik", "electricity", False, 740.17, 1008.00),
            MeterReadingInput("el_ania", "ap_ania", "electricity", False, 3631.76, 3761.16),
            MeterReadingInput("el_lukasz", "ap_lukasz", "electricity", True, 12600, 13169),
        ]

        result, err, ok = calculation_meter_consumptions(readings)

        assert ok is True
        by_id = {consumption.meter_id: consumption for consumption in result}
        # 569 - 267,83 - 129,4 = 171,77 (jak w notatce)
        assert by_id["el_lukasz"].consumption == 171.77

    def test_consumptions04_master_ignores_other_media(self):
        # nadrzędny licznik wody nie odejmuje zużycia prądu
        readings = [
            MeterReadingInput("w_master", "ap_a", "water", True, 100, 110),
            MeterReadingInput("el_b", "ap_b", "electricity", False, 200, 300),
        ]

        result, err, ok = calculation_meter_consumptions(readings)

        assert ok is True
        by_id = {consumption.meter_id: consumption for consumption in result}
        assert by_id["w_master"].consumption == 10

    def test_consumptions05_current_lower_than_previous_fails(self):
        readings = [MeterReadingInput("m1", "ap", "water", False, 10.5, 9.0)]

        result, err, ok = calculation_meter_consumptions(readings)

        assert ok is False and result is None
        assert "mniejszy" in err.message
        assert err.type_module == "calculation_meter_consumptions"

    def test_consumptions06_negative_master_consumption_fails(self):
        readings = [
            MeterReadingInput("w_master", "ap_a", "water", True, 100, 101),
            MeterReadingInput("w_b", "ap_b", "water", False, 50, 60),
        ]

        result, err, ok = calculation_meter_consumptions(readings)

        assert ok is False
        assert "Ujemne zużycie licznika nadrzędnego" in err.message

    def test_consumptions07_two_masters_same_media_fails(self):
        readings = [
            MeterReadingInput("w_a", "ap_a", "water", True, 0, 1),
            MeterReadingInput("w_b", "ap_b", "water", True, 0, 1),
        ]

        result, err, ok = calculation_meter_consumptions(readings)

        assert ok is False
        assert "nadrzędny" in err.message

    def test_consumptions08_empty_returns_empty(self):
        result, err, ok = calculation_meter_consumptions([])

        assert ok is True
        assert result == []


class TestCalculationMainMeterError:
    def test_error01_obliczenia3(self):
        # 858 - 855,73 = 2,27 (bez korekt)
        consumptions, _, _ = calculation_meter_consumptions(_obliczenia3_electricity())
        apartments = [c for c in consumptions if c.apartment_id is not None]

        result, err, ok = calculation_main_meter_error(858, apartments)

        assert ok is True and err is None
        assert result.apartments_total == 855.73
        assert result.error == 2.27
        assert len(result.proposals) == 4

    def test_error02_obliczenia_txt_skips_zero_consumption(self):
        # Obliczenia.txt: "Błąd_między_licznikami: 11,63" — surowe różnice odczytów dają
        # 558,37 (570 - 558,37 = 11,63); Mieszkanie_4 bez zużycia -> propozycja tylko dla 3
        readings = [
            MeterReadingInput("el_dudzik", "ap_dudzik", "electricity", False, 4852.72, 5164.98),
            MeterReadingInput("el_kydr", "ap_kydr", "electricity", False, 4958.04, 5073.04),
            MeterReadingInput("el_m4", "ap_m4", "electricity", False, 290.66, 290.66),
            MeterReadingInput("el_lukasz", "ap_lukasz", "electricity", False, 2726.01, 2857.12),
        ]
        consumptions, _, _ = calculation_meter_consumptions(readings)

        result, err, ok = calculation_main_meter_error(570, consumptions)

        assert ok is True
        assert result.apartments_total == 558.37
        assert result.error == 11.63
        assert len(result.proposals) == 3  # bez Mieszkania_4
        assert all(proposal.meter_id != "el_m4" for proposal in result.proposals)
        assert result.proposals[0].proposed_correction == round(11.63 / 3, 3)

    def test_error03_zero_error_no_proposals(self):
        readings = [MeterReadingInput("el_a", "ap_a", "electricity", False, 0, 100)]
        consumptions, _, _ = calculation_meter_consumptions(readings)

        result, err, ok = calculation_main_meter_error(100, consumptions)

        assert ok is True
        assert result.error == 0
        assert result.proposals == []

    def test_error04_negative_main_difference_fails(self):
        result, err, ok = calculation_main_meter_error(-5, [])

        assert ok is False
        assert "Ujemna różnica" in err.message


class TestCalculationElectricityRate:
    def test_rate01_obliczenia3(self):
        # koszt: 899,48 / 855,73 = 1,05 (dokładnie 1,0511)
        result, err, ok = calculation_electricity_rate(899.48, 855.73)

        assert ok is True and err is None
        assert result.rate == 1.0511

    def test_rate02_obliczenia_txt(self):
        # Do zapłaty: 586,92 / 568,37 kWh
        result, err, ok = calculation_electricity_rate(586.92, 568.37)

        assert ok is True
        assert result.rate == round(586.92 / 568.37, 4)

    def test_rate03_zero_consumption_fails(self):
        result, err, ok = calculation_electricity_rate(899.48, 0)

        assert ok is False
        assert "większa od zera" in err.message

    def test_rate04_negative_bill_fails(self):
        result, err, ok = calculation_electricity_rate(-1, 100)

        assert ok is False
        assert "Ujemna kwota" in err.message
