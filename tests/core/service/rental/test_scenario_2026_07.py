"""Scenariusz z ręcznych obliczeń lipca 2026 (Dudzik, Kydr, Witek, Puste + szymon_kasia).

Dane wejściowe od Artura:
- rachunek Tauron 544,94 zł, suma podliczników 412,72 kWh, ręczna stawka 1,31 zł/kWh,
- pokój "Puste" (dawny Łukasza): licznik prądu wyzerowany (Teraz: 0), woda nadrzędna,
- rozbieżności notatki opisane w komentarzach testów (stawka i ujemna woda nadrzędna).
"""

from core.service.rental.billing.calculation import calculation_apartment_settlement
from core.service.rental.billing.response import ApartmentCostInput
from core.service.rental.family.calculation import calculation_family_allocation
from core.service.rental.family.response import (
    AllocationRuleInput,
    AllocationSettlementInput,
    AllocationSettlementItemInput,
)
from core.service.rental.meters.calculation import (
    calculation_electricity_rate,
    calculation_meter_consumptions,
)
from core.service.rental.meters.response import MeterReadingInput


class TestScenarioElectricityRate:
    def test_rate01_computed_rate_is_higher_than_manual(self):
        # notatka: "koszt: 544,94 / 412,72 = 1,31" — faktyczny iloraz to 1,3204!
        # przy stawce 1,31 suma prądu (540 zł) nie pokrywa rachunku (544,94 zł)
        result, err, ok = calculation_electricity_rate(544.94, 412.72)

        assert ok is True and err is None
        assert result.rate == 1.3204

    def test_rate02_manual_rate_undercharges_bill(self):
        # suma z notatki: 332 + 46 + 162 = 540 zł < 544,94 zł (brakuje ~5 zł)
        electricity_sum = 332 + 46 + 162

        assert electricity_sum == 540
        assert electricity_sum < 544.94


class TestScenarioMeters:
    def test_meters01_electricity_consumptions(self):
        readings = [
            MeterReadingInput("el_dudzik", "ap_dudzik", "electricity", False, 10149.65, 10403.19),
            MeterReadingInput("el_kydr", "ap_kydr", "electricity", False, 6418.01, 6453.31),
            MeterReadingInput("el_witek", "ap_witek", "electricity", False, 5071.21, 5195.09),
            # licznik "Puste" wyzerowany (Teraz: 0) — zużycie 0 wpisujemy jako 0/0,
            # bo odczyt Teraz < Ostatnio system odrzuca
            MeterReadingInput("el_puste", "ap_puste", "electricity", False, 0, 0),
        ]

        result, err, ok = calculation_meter_consumptions(readings)

        assert ok is True and err is None
        by_id = {consumption.meter_id: consumption for consumption in result}
        assert by_id["el_dudzik"].consumption == 253.54
        assert by_id["el_kydr"].consumption == 35.3
        assert by_id["el_witek"].consumption == 123.88
        assert by_id["el_puste"].consumption == 0
        # suma czterech liczników jak w notatce: 412,72
        assert round(sum(c.consumption for c in result), 3) == 412.72

    def test_meters02_reset_meter_raw_readings_rejected(self):
        # surowy odczyt "Puste": Ostatnio 8217,47 -> Teraz 0 (wymiana/zerowanie licznika)
        readings = [MeterReadingInput("el_puste", "ap_puste", "electricity", False, 8217.47, 0)]

        result, err, ok = calculation_meter_consumptions(readings)

        assert ok is False
        assert "mniejszy" in err.message

    def test_meters03_master_water_is_negative_in_this_month(self):
        # notatka: 727,048 - 716,667 - 4,083 - 0,193 - 6,286 = "0"
        # naprawdę: 10,381 - 10,562 = -0,181 — podliczniki wskazały WIĘCEJ niż licznik główny
        readings = [
            MeterReadingInput("w_dudzik", "ap_dudzik", "water", False, 234.388, 240.674),
            MeterReadingInput("w_kydr", "ap_kydr", "water", False, 94.791, 94.984),
            MeterReadingInput("w_witek", "ap_witek", "water", False, 142.357, 146.440),
            MeterReadingInput("w_puste", "ap_puste", "water", True, 716.667, 727.048),
        ]

        result, err, ok = calculation_meter_consumptions(readings)

        assert ok is False and result is None
        assert "Ujemne zużycie licznika nadrzędnego" in err.message

    def test_meters04_master_water_zero_with_error_correction(self):
        # korekta +0,181 (błąd tolerancji liczników) daje 0 — jak w notatce
        readings = [
            MeterReadingInput("w_dudzik", "ap_dudzik", "water", False, 234.388, 240.674),
            MeterReadingInput("w_kydr", "ap_kydr", "water", False, 94.791, 94.984),
            MeterReadingInput("w_witek", "ap_witek", "water", False, 142.357, 146.440),
            MeterReadingInput("w_puste", "ap_puste", "water", True, 716.667, 727.048, 0.181),
        ]

        result, err, ok = calculation_meter_consumptions(readings)

        assert ok is True
        by_id = {consumption.meter_id: consumption for consumption in result}
        assert by_id["w_dudzik"].consumption == 6.286
        assert by_id["w_kydr"].consumption == 0.193
        assert by_id["w_witek"].consumption == 4.083
        assert by_id["w_puste"].consumption == 0


class TestScenarioBilling:
    def test_billing01_dudzik(self):
        # Razem: 332 + 57 + 70 + 60 + 200 = 719
        result, err, ok = calculation_apartment_settlement(
            apartment_id="ap_dudzik",
            electricity_consumption=253.54,
            electricity_rate=1.31,
            water_consumption=6.286,
            water_rate=9.0,
            fixed_costs=[
                ApartmentCostInput("ct_smieci", "śmieci", "per_person", 35),
                ApartmentCostInput("ct_internet", "internet", "fixed", 60),
                ApartmentCostInput("ct_garaz", "garaż", "fixed", 200),
            ],
            adjustments=[],
            tenancy_id="t_dudzik",
            rent_amount=1000,
            persons_count=2,
        )

        assert ok is True and err is None
        assert result.electricity_cost == 332.0  # 332,1374 ~ 332
        assert result.water_cost == 57.0  # 56,574 ~ 57
        assert result.total_media_amount == 719.0

    def test_billing02_kydr(self):
        # Razem: 46 + 2 + 35 + 0 = 83
        result, err, ok = calculation_apartment_settlement(
            apartment_id="ap_kydr",
            electricity_consumption=35.3,
            electricity_rate=1.31,
            water_consumption=0.193,
            water_rate=9.0,
            fixed_costs=[ApartmentCostInput("ct_smieci", "śmieci", "per_person", 35)],
            adjustments=[],
            tenancy_id="t_kydr",
            rent_amount=1000,
            persons_count=1,
        )

        assert ok is True
        assert result.electricity_cost == 46.0  # 46,243 ~ 46
        assert result.water_cost == 2.0  # 1,737 ~ 2
        assert result.total_media_amount == 83.0

    def test_billing03_witek_two_persons(self):
        # Razem: 162 + 37 + 70 + 0 = 269 (śmieci 2 x 35 — u Witka są teraz 2 osoby)
        result, err, ok = calculation_apartment_settlement(
            apartment_id="ap_witek",
            electricity_consumption=123.88,
            electricity_rate=1.31,
            water_consumption=4.083,
            water_rate=9.0,
            fixed_costs=[ApartmentCostInput("ct_smieci", "śmieci", "per_person", 35)],
            adjustments=[],
            tenancy_id="t_witek",
            rent_amount=1000,
            persons_count=2,
        )

        assert ok is True
        assert result.electricity_cost == 162.0  # 162,2828 ~ 162
        assert result.water_cost == 37.0  # 36,747 ~ 37
        assert result.total_media_amount == 269.0

    def test_billing04_puste_vacant(self):
        # Razem: 35 + 60 = 95 (pustostan: media zerowe, tylko śmieci i internet)
        result, err, ok = calculation_apartment_settlement(
            apartment_id="ap_puste",
            electricity_consumption=0,
            electricity_rate=1.31,
            water_consumption=0,
            water_rate=9.0,
            fixed_costs=[
                ApartmentCostInput("ct_smieci", "śmieci", "per_person", 35),
                ApartmentCostInput("ct_internet", "internet", "fixed", 60),
            ],
            adjustments=[],
        )

        assert ok is True
        assert result.tenancy_id is None
        assert result.total_media_amount == 95.0


class TestScenarioFamily:
    @staticmethod
    def _settlements() -> list[AllocationSettlementInput]:
        return [
            AllocationSettlementInput(
                apartment_id="ap_dudzik",
                apartment_name="Pokój Państwa Dudzik",
                rent_amount=1000,
                electricity_cost=332,
                water_cost=57,
                settlement_id="s_dudzik",
                items=[
                    AllocationSettlementItemInput("śmieci (2 os. x 35 zł)", "fixed_cost", 70, "ct_smieci"),
                    AllocationSettlementItemInput("internet", "fixed_cost", 60, "ct_internet"),
                    AllocationSettlementItemInput("garaż", "fixed_cost", 200, "ct_garaz"),
                ],
            ),
            AllocationSettlementInput(
                apartment_id="ap_kydr",
                apartment_name="Pokój Łukasza Kydr",
                rent_amount=1000,
                electricity_cost=46,
                water_cost=2,
                settlement_id="s_kydr",
                items=[AllocationSettlementItemInput("śmieci", "fixed_cost", 35, "ct_smieci")],
            ),
            AllocationSettlementInput(
                apartment_id="ap_witek",
                apartment_name="Pokój Witka",
                rent_amount=1000,
                electricity_cost=162,
                water_cost=37,
                settlement_id="s_witek",
                items=[AllocationSettlementItemInput("śmieci (2 os. x 35 zł)", "fixed_cost", 70, "ct_smieci")],
            ),
            AllocationSettlementInput(
                apartment_id="ap_puste",
                apartment_name="Pokój Pusty",
                rent_amount=0,
                electricity_cost=0,
                water_cost=0,
                settlement_id="s_puste",
                items=[
                    AllocationSettlementItemInput("śmieci", "fixed_cost", 35, "ct_smieci"),
                    AllocationSettlementItemInput("internet", "fixed_cost", 60, "ct_internet"),
                ],
            ),
        ]

    @staticmethod
    def _rules() -> list[AllocationRuleInput]:
        return [
            # Ja: czynsz szymon_kasia 1000 (osobna nieruchomość), cały prąd, podatek -90, telefon -25
            AllocationRuleInput(
                "r_ja_szymon", "ja", "recurring", "fixed_amount", amount=1000, description="czynsz szymon_kasia"
            ),
            AllocationRuleInput("r_ja_prad", "ja", "electricity", "full"),
            AllocationRuleInput("r_ja_podatek", "ja", "recurring", "fixed_amount", amount=-90, description="podatek"),
            AllocationRuleInput("r_ja_telefon", "ja", "recurring", "fixed_amount", amount=-25, description="telefon"),
            # Ojciec: czynsze Kydr/Dudzik/Witek po 1000, garaż, podatek -270
            AllocationRuleInput("r_oj_kydr", "ojciec", "rent", "fixed_amount", "ap_kydr", amount=1000),
            AllocationRuleInput("r_oj_dudzik", "ojciec", "rent", "fixed_amount", "ap_dudzik", amount=1000),
            AllocationRuleInput("r_oj_witek", "ojciec", "rent", "fixed_amount", "ap_witek", amount=1000),
            AllocationRuleInput(
                "r_oj_garaz", "ojciec", "cost_type", "full", cost_type_id="ct_garaz", description="garaż"
            ),
            AllocationRuleInput(
                "r_oj_podatek", "ojciec", "recurring", "fixed_amount", amount=-270, description="podatek"
            ),
            # Mama: podatek +360, telefon +25, woda + śmieci + internet ze wszystkich mieszkań
            AllocationRuleInput("r_ma_podatek", "mama", "recurring", "fixed_amount", amount=360, description="podatek"),
            AllocationRuleInput("r_ma_telefon", "mama", "recurring", "fixed_amount", amount=25, description="telefon"),
            AllocationRuleInput("r_ma_woda", "mama", "water", "full"),
            AllocationRuleInput(
                "r_ma_smieci", "mama", "cost_type", "full", cost_type_id="ct_smieci", description="śmieci"
            ),
            AllocationRuleInput(
                "r_ma_internet", "mama", "cost_type", "full", cost_type_id="ct_internet", description="internet"
            ),
        ]

    def test_family01_totals(self):
        result, err, ok = calculation_family_allocation(self._rules(), self._settlements())

        assert ok is True and err is None
        totals = {beneficiary.beneficiary_id: beneficiary.total_amount for beneficiary in result.beneficiaries}
        # Ja: 1000 + prąd (332+46+162+0 = 540) - 90 - 25 = 1425
        assert totals["ja"] == 1425.0
        # Ojciec: 1000 + 1000 + 1000 + garaż 200 - 270 = 2930
        assert totals["ojciec"] == 2930.0
        # Mama: 360 + 25 + woda 96 + śmieci 210 + internet 120 = 811 (jak "Razem: 811" w notatce)
        assert totals["mama"] == 811.0

    def test_family02_electricity_for_ja_matches_note_sum(self):
        result, _, ok = calculation_family_allocation(self._rules(), self._settlements())

        assert ok is True
        ja = next(b for b in result.beneficiaries if b.beneficiary_id == "ja")
        electricity_items = [item for item in ja.items if item.rule_id == "r_ja_prad"]
        # "prąd dla mnie": 332 + 46 + 162 + 0 = 540
        assert sum(item.amount for item in electricity_items) == 540.0

    def test_family03_mama_items_match_note(self):
        result, _, ok = calculation_family_allocation(self._rules(), self._settlements())

        assert ok is True
        mama = next(b for b in result.beneficiaries if b.beneficiary_id == "mama")
        water = sorted(item.amount for item in mama.items if item.rule_id == "r_ma_woda")
        garbage = sorted(item.amount for item in mama.items if item.rule_id == "r_ma_smieci")
        internet = sorted(item.amount for item in mama.items if item.rule_id == "r_ma_internet")
        assert water == [0.0, 2.0, 37.0, 57.0]  # pokój, Kydr, Witek, Dudzik
        assert garbage == [35.0, 35.0, 70.0, 70.0]
        assert internet == [0.0, 0.0, 60.0, 60.0]

    def test_family04_no_rent_warnings(self):
        # czynsze rozdzielone w całości: Dudzik/Kydr/Witek po 1000 -> Ojciec, Puste 0
        result, _, ok = calculation_family_allocation(self._rules(), self._settlements())

        assert ok is True
        assert result.warnings == []
