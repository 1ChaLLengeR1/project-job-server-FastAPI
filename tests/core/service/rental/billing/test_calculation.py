"""Testy rozliczeń mieszkań na realnych danych z docs/Obliczenia*.txt."""

from core.service.rental.billing.calculation import (
    calculation_apartment_settlement,
    calculation_fixed_costs,
    calculation_media_cost,
)
from core.service.rental.billing.response import AdjustmentInput, ApartmentCostInput


class TestCalculationMediaCost:
    def test_media01_electricity_dudzik_obliczenia3(self):
        # 318,6 * 1,05 = 334,53 ~ 335
        result, err, ok = calculation_media_cost(318.6, 1.05)

        assert ok is True and err is None
        assert result.cost == 335.0

    def test_media02_water_dudzik_obliczenia3(self):
        # 7,125 * 9 = 64,125 ~ 64
        result, err, ok = calculation_media_cost(7.125, 9.0)

        assert ok is True
        assert result.cost == 64.0

    def test_media03_electricity_kydr_rounds_half_up(self):
        # 85,35 * 1,05 = 89,6175 ~ 90
        result, err, ok = calculation_media_cost(85.35, 1.05)

        assert ok is True
        assert result.cost == 90.0

    def test_media04_water_ania_obliczenia1(self):
        # 2,621 * 9 = 23,589 ~ 24
        result, err, ok = calculation_media_cost(2.621, 9.0)

        assert ok is True
        assert result.cost == 24.0

    def test_media05_zero_consumption_zero_cost(self):
        # woda Kydra z Obliczenia_3: 0,045 zaokrąglone przez Artura do 0 kubika
        result, err, ok = calculation_media_cost(0, 9.0)

        assert ok is True
        assert result.cost == 0.0

    def test_media06_negative_consumption_fails(self):
        result, err, ok = calculation_media_cost(-1, 9.0)

        assert ok is False
        assert "Ujemne zużycie" in err.message

    def test_media07_negative_rate_fails(self):
        result, err, ok = calculation_media_cost(1, -9.0)

        assert ok is False
        assert "Ujemna stawka" in err.message


class TestCalculationFixedCosts:
    def test_fixed01_per_person_smieci_dudzik(self):
        # Śmieci(osoba: 35): 70zł — 2 osoby (Obliczenia_3)
        result, err, ok = calculation_fixed_costs(
            [ApartmentCostInput("ct_smieci", "śmieci", "per_person", 35)], persons_count=2
        )

        assert ok is True and err is None
        assert result[0].amount == 70.0
        assert result[0].kind == "fixed_cost"
        assert "2 os." in result[0].name

    def test_fixed02_fixed_amounts(self):
        result, err, ok = calculation_fixed_costs(
            [
                ApartmentCostInput("ct_internet", "internet", "fixed", 60),
                ApartmentCostInput("ct_garaz", "garaż", "fixed", 200),
                ApartmentCostInput("ct_przesyl", "przesył", "fixed", 9),
            ],
            persons_count=1,
        )

        assert ok is True
        assert [item.amount for item in result] == [60.0, 200.0, 9.0]
        assert result[0].name == "internet"

    def test_fixed03_unknown_charge_type_fails(self):
        result, err, ok = calculation_fixed_costs([ApartmentCostInput("ct", "śmieci", "per_m2", 35)], persons_count=1)

        assert ok is False
        assert "Nieznany typ naliczania" in err.message

    def test_fixed04_persons_count_below_one_fails(self):
        result, err, ok = calculation_fixed_costs([], persons_count=0)

        assert ok is False
        assert "co najmniej 1" in err.message


class TestCalculationApartmentSettlement:
    def test_settlement01_dudzik_obliczenia3(self):
        # Razem: 335 + 64 + 70 + 60 + 200 - 200 = 529
        result, err, ok = calculation_apartment_settlement(
            apartment_id="ap_dudzik",
            electricity_consumption=318.6,
            electricity_rate=1.05,
            water_consumption=7.125,
            water_rate=9.0,
            fixed_costs=[
                ApartmentCostInput("ct_smieci", "śmieci", "per_person", 35),
                ApartmentCostInput("ct_internet", "internet", "fixed", 60),
                ApartmentCostInput("ct_garaz", "garaż", "fixed", 200),
            ],
            adjustments=[AdjustmentInput("rabat garaż", -200)],
            tenancy_id="t_dudzik",
            rent_amount=1300,
            persons_count=2,
        )

        assert ok is True and err is None
        assert result.electricity_cost == 335.0
        assert result.water_cost == 64.0
        assert result.total_media_amount == 529.0
        assert result.total_amount == 1829.0  # 529 + czynsz 1300
        assert len(result.items) == 4

    def test_settlement02_ania_obliczenia1_with_overpayment(self):
        # Razem: 123 + 24 + 9 + 27 + 30 - 19(nadpłata) = 194
        result, err, ok = calculation_apartment_settlement(
            apartment_id="ap_ania",
            electricity_consumption=129.4,
            electricity_rate=0.95,
            water_consumption=2.621,
            water_rate=9.0,
            fixed_costs=[
                ApartmentCostInput("ct_przesyl", "przesył", "fixed", 9),
                ApartmentCostInput("ct_smieci", "śmieci", "fixed", 27),
                ApartmentCostInput("ct_internet", "internet", "fixed", 30),
            ],
            adjustments=[AdjustmentInput("nadpłata", -19)],
            tenancy_id="t_ania",
            rent_amount=1000,
        )

        assert ok is True
        assert result.electricity_cost == 123.0  # 122,93 ~ 123
        assert result.water_cost == 24.0
        assert result.total_media_amount == 194.0

    def test_settlement03_kydr_obliczenia3(self):
        # Razem: 90 + 0 + 35 = 125
        result, err, ok = calculation_apartment_settlement(
            apartment_id="ap_kydr",
            electricity_consumption=85.35,
            electricity_rate=1.05,
            water_consumption=0,
            water_rate=9.0,
            fixed_costs=[ApartmentCostInput("ct_smieci", "śmieci", "per_person", 35)],
            adjustments=[],
            tenancy_id="t_kydr",
            rent_amount=1000,
            persons_count=1,
        )

        assert ok is True
        assert result.total_media_amount == 125.0
        assert result.total_amount == 1125.0

    def test_settlement04_vacant_apartment_mieszkanie4(self):
        # Mieszkanie_4 z Obliczenia.txt: pustostan, tylko śmieci 27
        result, err, ok = calculation_apartment_settlement(
            apartment_id="ap_m4",
            electricity_consumption=0,
            electricity_rate=0.80,
            water_consumption=0.002,
            water_rate=9.0,
            fixed_costs=[ApartmentCostInput("ct_smieci", "śmieci", "fixed", 27)],
            adjustments=[],
        )

        assert ok is True
        assert result.tenancy_id is None
        assert result.rent_amount == 0.0
        assert result.total_media_amount == 27.0
        assert result.total_amount == 27.0

    def test_settlement05_propagates_media_error(self):
        result, err, ok = calculation_apartment_settlement(
            apartment_id="ap",
            electricity_consumption=-1,
            electricity_rate=1.05,
            water_consumption=0,
            water_rate=9.0,
            fixed_costs=[],
            adjustments=[],
        )

        assert ok is False
        assert err.type_module == "calculation_media_cost"
