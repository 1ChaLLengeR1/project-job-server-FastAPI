from core.repository.psql.patryk.response import KeysCalculatorResponse
from core.service.patryk.calculation import (
    _shipping_cost,
    _smart_package_price,
    calculation_profit,
)


def make_keys(**overrides) -> KeysCalculatorResponse:
    defaults = {
        "id": "6fa459ea-ee8a-4ca4-894e-db77e160355e",
        "income_tax": 0.12,
        "vat": 0.23,
        "inpost_parcel_locker": 12.99,
        "inpost_courier": 15.99,
        "inpost_cash_of_delivery_courier": 19.99,
        "dpd": 14.99,
        "allegro_matt": 9.99,
        "without_smart": 11.99,
    }
    defaults.update(overrides)
    return KeysCalculatorResponse(**defaults)


class TestSmartPackagePrice:
    def test_package01_thresholds(self):
        assert _smart_package_price(40.0) == 0.99
        assert _smart_package_price(79.99) == 0.99
        assert _smart_package_price(80.0) == 2.49
        assert _smart_package_price(199.99) == 2.49
        assert _smart_package_price(200.0) == 3.99
        assert _smart_package_price(299.99) == 3.99
        assert _smart_package_price(300.0) == 4.99
        assert _smart_package_price(1000.0) == 4.99


class TestShippingCost:
    def test_shipping01_returns_price_for_each_referrer(self):
        keys = make_keys()

        assert _shipping_cost(keys, "inpost_parcel_locker") == 12.99
        assert _shipping_cost(keys, "dpd") == 14.99
        assert _shipping_cost(keys, "without_smart") == 11.99

    def test_shipping02_unknown_referrer_returns_zero(self):
        assert _shipping_cost(make_keys(), "golab_pocztowy") == 0


class TestCalculationProfit:
    def test_profit01_below_smart_threshold_uses_shipping_cost(self):
        keys = make_keys()
        gross_sales, gross_purchase, provision = 30.0, 15.0, 10.0

        result, err, ok = calculation_profit(keys, gross_sales, gross_purchase, provision, 0.0, "dpd")

        assert ok is True and err is None
        # formuła gałęzi < 40 zł policzona wprost
        vat, dochodowka = keys.vat, keys.income_tax
        cena_netto_zakup = gross_purchase - gross_purchase * vat
        cena_netto_sprzedarz = gross_sales - gross_sales * vat
        z_wysylka_prowizja = (gross_sales + keys.dpd) * (provision / 100)
        rv_wysylki = z_wysylka_prowizja * vat
        przychod = cena_netto_sprzedarz - cena_netto_zakup - (z_wysylka_prowizja - rv_wysylki)
        dochod = przychod - przychod * dochodowka
        zysk = dochod - (gross_sales * vat - gross_purchase * vat - rv_wysylki)
        assert result.na_czysto == round(zysk, 2)
        assert result.brutto == round(zysk * 1.23, 2)
        assert result.zysk_procentowy == round((zysk * 100) / cena_netto_zakup, 2)

    def test_profit02_above_smart_threshold_uses_package_price(self):
        keys = make_keys()
        gross_sales, gross_purchase, provision, distinction = 100.0, 50.0, 10.0, 2.0

        result, err, ok = calculation_profit(keys, gross_sales, gross_purchase, provision, distinction, "dpd")

        assert ok is True and err is None
        # formuła gałęzi >= 40 zł (cena paczki 2.49 dla 100 zł)
        vat, dochodowka = keys.vat, keys.income_tax
        cena_netto_zakup = gross_purchase - gross_purchase * vat
        cena_netto_sprzedarz = gross_sales - gross_sales * vat
        suma_pw = gross_sales * (provision / 100) + gross_sales * (distinction / 100)
        rv_pw = suma_pw * vat
        pw_netto = suma_pw - rv_pw
        cena_paczki = 2.49
        pv = cena_paczki * vat
        przychod = cena_netto_sprzedarz - cena_netto_zakup - pw_netto - (cena_paczki - pv)
        dochod = przychod - przychod * dochodowka
        zysk = dochod - (gross_sales * vat - gross_purchase * vat - rv_pw - pv)
        assert result.na_czysto == round(zysk, 2)
        assert result.brutto == round(zysk * 1.23, 2)

    def test_profit03_referrer_ignored_above_threshold(self):
        keys = make_keys()

        result_dpd, _, _ = calculation_profit(keys, 100.0, 50.0, 10.0, 0.0, "dpd")
        result_inpost, _, _ = calculation_profit(keys, 100.0, 50.0, 10.0, 0.0, "inpost_courier")

        assert result_dpd == result_inpost

    def test_profit04_zero_purchase_returns_exception_error(self):
        # dzielenie przez zero w zysku procentowym — payload tego broni (gt=0),
        # ale service ma zwrócić kontrolowany błąd, nie wyjątek
        result, err, ok = calculation_profit(make_keys(), 100.0, 0.0, 10.0, 0.0, "dpd")

        assert ok is False and result is None
        assert err.key_type_error == "Exception"
        assert err.type_module == "calculation_profit"
