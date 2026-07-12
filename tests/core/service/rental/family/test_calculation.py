"""Testy podziału rodzinnego na realnych danych z docs/Obliczenia_3.txt (sekcje Ja/Ojciec/Mama)."""

from core.service.rental.family.calculation import calculation_family_allocation
from core.service.rental.family.response import (
    AllocationRuleInput,
    AllocationSettlementInput,
    AllocationSettlementItemInput,
)


def _obliczenia3_settlements() -> list[AllocationSettlementInput]:
    """Rozliczenia czterech mieszkań z Obliczenia_3 (czerwiec 2026)."""
    return [
        AllocationSettlementInput(
            apartment_id="ap_dudzik",
            apartment_name="Pokój Państwa Dudzik",
            rent_amount=1300,
            electricity_cost=335,
            water_cost=64,
            settlement_id="s_dudzik",
            items=[
                AllocationSettlementItemInput("śmieci (2 os. x 35 zł)", "fixed_cost", 70, "ct_smieci"),
                AllocationSettlementItemInput("internet", "fixed_cost", 60, "ct_internet"),
                AllocationSettlementItemInput("garaż", "fixed_cost", 200, "ct_garaz"),
                AllocationSettlementItemInput("rabat garaż", "adjustment", -200),
            ],
        ),
        AllocationSettlementInput(
            apartment_id="ap_kydr",
            apartment_name="Pokój Łukasza Kydr",
            rent_amount=1000,
            electricity_cost=90,
            water_cost=0,
            settlement_id="s_kydr",
            items=[AllocationSettlementItemInput("śmieci", "fixed_cost", 35, "ct_smieci")],
        ),
        AllocationSettlementInput(
            apartment_id="ap_witek",
            apartment_name="Pokój Witka",
            rent_amount=1000,
            electricity_cost=292,
            water_cost=74,
            settlement_id="s_witek",
            items=[AllocationSettlementItemInput("śmieci", "fixed_cost", 35, "ct_smieci")],
        ),
        AllocationSettlementInput(
            apartment_id="ap_lukasz",
            apartment_name="Pokój Łukasza",
            rent_amount=1000,
            electricity_cost=186,
            water_cost=22,
            settlement_id="s_lukasz",
            items=[
                AllocationSettlementItemInput("śmieci", "fixed_cost", 35, "ct_smieci"),
                AllocationSettlementItemInput("internet", "fixed_cost", 60, "ct_internet"),
            ],
        ),
    ]


def _obliczenia3_rules() -> list[AllocationRuleInput]:
    """Reguły podziału odtworzone z sekcji Ja/Ojciec/Mama."""
    return [
        # Ja: czynsz Łukasz 1000, czynsz Dudzik 100, cały prąd, podatek -90, telefon -25
        AllocationRuleInput("r_ja_lukasz", "ja", "rent", "fixed_amount", "ap_lukasz", amount=1000),
        AllocationRuleInput("r_ja_dudzik", "ja", "rent", "fixed_amount", "ap_dudzik", amount=100),
        AllocationRuleInput("r_ja_prad", "ja", "electricity", "full"),
        AllocationRuleInput("r_ja_podatek", "ja", "recurring", "fixed_amount", amount=-90, description="podatek"),
        AllocationRuleInput("r_ja_telefon", "ja", "recurring", "fixed_amount", amount=-25, description="telefon"),
        # Ojciec: czynsz Kydr 1000, czynsz Dudzik 1100, czynsz Witek 1000, garaż, podatek -270
        AllocationRuleInput("r_oj_kydr", "ojciec", "rent", "fixed_amount", "ap_kydr", amount=1000),
        AllocationRuleInput("r_oj_dudzik", "ojciec", "rent", "fixed_amount", "ap_dudzik", amount=1100),
        AllocationRuleInput("r_oj_witek", "ojciec", "rent", "fixed_amount", "ap_witek", amount=1000),
        AllocationRuleInput("r_oj_garaz", "ojciec", "cost_type", "full", cost_type_id="ct_garaz", description="garaż"),
        AllocationRuleInput("r_oj_podatek", "ojciec", "recurring", "fixed_amount", amount=-270, description="podatek"),
        # Mama: czynsz Dudzik 100, podatek +360, telefon +25, woda + śmieci + internet ze wszystkich
        AllocationRuleInput("r_ma_dudzik", "mama", "rent", "fixed_amount", "ap_dudzik", amount=100),
        AllocationRuleInput("r_ma_podatek", "mama", "recurring", "fixed_amount", amount=360, description="podatek"),
        AllocationRuleInput("r_ma_telefon", "mama", "recurring", "fixed_amount", amount=25, description="telefon"),
        AllocationRuleInput("r_ma_woda", "mama", "water", "full"),
        AllocationRuleInput("r_ma_smieci", "mama", "cost_type", "full", cost_type_id="ct_smieci", description="śmieci"),
        AllocationRuleInput(
            "r_ma_internet", "mama", "cost_type", "full", cost_type_id="ct_internet", description="internet"
        ),
    ]


class TestCalculationFamilyAllocation:
    def test_allocation01_obliczenia3_totals(self):
        result, err, ok = calculation_family_allocation(_obliczenia3_rules(), _obliczenia3_settlements())

        assert ok is True and err is None
        totals = {beneficiary.beneficiary_id: beneficiary.total_amount for beneficiary in result.beneficiaries}
        # Ja: 1000 + 100 + prąd (335+90+292+186=903) - 90 - 25 = 1888
        assert totals["ja"] == 1888.0
        # Ojciec: 1000 + 1100 + 1000 + garaż 200 - 270 = 3030
        assert totals["ojciec"] == 3030.0
        # Mama: 100 + 360 + 25 + woda 160 + śmieci 175 + internet 120 = 940 (jak "Razem: 940" w notatce)
        assert totals["mama"] == 940.0

    def test_allocation02_full_electricity_item_per_apartment(self):
        result, _, ok = calculation_family_allocation(_obliczenia3_rules(), _obliczenia3_settlements())

        assert ok is True
        ja = next(b for b in result.beneficiaries if b.beneficiary_id == "ja")
        electricity_items = [item for item in ja.items if item.rule_id == "r_ja_prad"]
        # pozycja per mieszkanie, jak "prąd dla mnie: 335 + 90 + 292 + 186" w notatce
        assert len(electricity_items) == 4
        assert sorted(item.amount for item in electricity_items) == [90.0, 186.0, 292.0, 335.0]
        assert all(item.settlement_id is not None for item in electricity_items)

    def test_allocation03_cost_type_includes_zero_for_apartments_without_cost(self):
        result, _, ok = calculation_family_allocation(_obliczenia3_rules(), _obliczenia3_settlements())

        assert ok is True
        mama = next(b for b in result.beneficiaries if b.beneficiary_id == "mama")
        internet_items = [item for item in mama.items if item.rule_id == "r_ma_internet"]
        # jak w notatce: internet-dudzik 60, internet-Kier 0, internet-witek 0, internet-łukasz 60
        assert len(internet_items) == 4
        assert sorted(item.amount for item in internet_items) == [0.0, 0.0, 60.0, 60.0]

    def test_allocation04_no_warnings_when_rent_fully_allocated(self):
        result, _, ok = calculation_family_allocation(_obliczenia3_rules(), _obliczenia3_settlements())

        assert ok is True
        # Dudzik: 100+1100+100=1300, pozostałe po 1000 — wszystko się zgadza
        assert result.warnings == []

    def test_allocation05_warning_on_rent_mismatch(self):
        rules = [AllocationRuleInput("r1", "ojciec", "rent", "fixed_amount", "ap_dudzik", amount=1100)]
        settlements = [
            AllocationSettlementInput(
                apartment_id="ap_dudzik",
                apartment_name="Pokój Państwa Dudzik",
                rent_amount=1300,
                electricity_cost=0,
                water_cost=0,
            )
        ]

        result, _, ok = calculation_family_allocation(rules, settlements)

        assert ok is True
        assert len(result.warnings) == 1
        assert "1100" in result.warnings[0] and "1300" in result.warnings[0]

    def test_allocation06_recurring_uses_description(self):
        rules = [
            AllocationRuleInput("r1", "mama", "recurring", "fixed_amount", amount=360, description="podatek"),
            AllocationRuleInput("r2", "mama", "recurring", "fixed_amount", amount=25),
        ]

        result, _, ok = calculation_family_allocation(rules, [])

        assert ok is True
        mama = result.beneficiaries[0]
        assert mama.items[0].description == "podatek"
        assert mama.items[1].description == "kwota stała"  # fallback bez opisu
        assert mama.total_amount == 385.0

    def test_allocation07_beneficiary_with_rules_but_no_matches_has_zero_total(self):
        rules = [AllocationRuleInput("r1", "ja", "electricity", "full", "ap_nieistniejace")]

        result, _, ok = calculation_family_allocation(rules, _obliczenia3_settlements())

        assert ok is True
        assert result.beneficiaries[0].total_amount == 0.0
        assert result.beneficiaries[0].items == []

    def test_allocation08_unknown_component_fails(self):
        rules = [AllocationRuleInput("r1", "ja", "gaz", "full")]

        result, err, ok = calculation_family_allocation(rules, [])

        assert ok is False
        assert "Nieznany składnik" in err.message

    def test_allocation09_fixed_amount_without_amount_fails(self):
        rules = [AllocationRuleInput("r1", "ja", "rent", "fixed_amount")]

        result, err, ok = calculation_family_allocation(rules, [])

        assert ok is False
        assert "wymaga kwoty" in err.message

    def test_allocation10_cost_type_without_cost_type_id_fails(self):
        rules = [AllocationRuleInput("r1", "mama", "cost_type", "full")]

        result, err, ok = calculation_family_allocation(rules, [])

        assert ok is False
        assert "cost_type_id" in err.message
