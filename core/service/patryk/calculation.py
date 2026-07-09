from api.response import ApiErrorData
from core.repository.psql.patryk.response import KeysCalculatorResponse
from core.service.patryk.response import CalculationResponse

# Koszty paczki Allegro Smart wg progów ceny sprzedaży brutto
_SMART_PACKAGE_PRICES = [
    (40.0, 79.99, 0.99),
    (80.0, 199.99, 2.49),
    (200.0, 299.99, 3.99),
]
_SMART_PACKAGE_PRICE_MAX = 4.99

_SHIPPING_FIELDS = (
    "inpost_parcel_locker",
    "inpost_courier",
    "inpost_cash_of_delivery_courier",
    "dpd",
    "allegro_matt",
    "without_smart",
)


def _shipping_cost(keys: KeysCalculatorResponse, referrer: str) -> float:
    if referrer in _SHIPPING_FIELDS:
        return getattr(keys, referrer)
    return 0


def _smart_package_price(gross_sales: float) -> float:
    for low, high, price in _SMART_PACKAGE_PRICES:
        if low <= gross_sales <= high:
            return price
    return _SMART_PACKAGE_PRICE_MAX


def calculation_profit(
    keys: KeysCalculatorResponse,
    gross_sales: float,
    gross_purchase: float,
    provision: float,
    distinction: float,
    referrer: str,
) -> tuple[CalculationResponse | None, ApiErrorData | None, bool]:
    try:
        dochodowka = keys.income_tax
        vat = keys.vat

        roznica_vat_zakupu = gross_purchase * vat
        cena_netto_zakup = gross_purchase - roznica_vat_zakupu
        roznica_vat_sprzedarz = gross_sales * vat
        cena_netto_sprzedarz = gross_sales - roznica_vat_sprzedarz
        prowizja_brutto = gross_sales * (provision / 100)
        wyroznienie_brutto = gross_sales * (distinction / 100)
        suma_prowizji_wyroznienie = prowizja_brutto + wyroznienie_brutto
        roznica_vat_prowizji_wyroznienie = suma_prowizji_wyroznienie * vat
        prowizja_wyroznienie_netto = suma_prowizji_wyroznienie - roznica_vat_prowizji_wyroznienie

        if gross_sales < 40:
            # Poniżej progu Smart: koszt wysyłki wg cennika przewoźnika (referrer)
            koszt_wysylki = _shipping_cost(keys, referrer)
            cena_sprzedarzy_brutto_z_wysylka = gross_sales + koszt_wysylki
            cena_sprzedarzy_brutto_z_wysylka_prowizja = cena_sprzedarzy_brutto_z_wysylka * (provision / 100)
            roznica_vat_wysylki = cena_sprzedarzy_brutto_z_wysylka_prowizja * vat
            netto_wysylka = cena_sprzedarzy_brutto_z_wysylka_prowizja - roznica_vat_wysylki
            przychod_netto = cena_netto_sprzedarz - cena_netto_zakup - netto_wysylka
            dochodowka_do_zaplacenia = przychod_netto * dochodowka
            dochod = przychod_netto - dochodowka_do_zaplacenia
            roznica_vat = roznica_vat_sprzedarz - roznica_vat_zakupu - roznica_vat_wysylki
            zysk = dochod - roznica_vat
        else:
            cena_paczki = _smart_package_price(gross_sales)
            prog_pierwszy_vat = cena_paczki * vat
            prog_pierwszy_cena_netto = cena_paczki - prog_pierwszy_vat
            przychod_netto = (
                cena_netto_sprzedarz - cena_netto_zakup - prowizja_wyroznienie_netto - prog_pierwszy_cena_netto
            )
            dochodowka_do_zaplaty = przychod_netto * dochodowka
            dochod = przychod_netto - dochodowka_do_zaplaty
            roznica_vat = (
                roznica_vat_sprzedarz - roznica_vat_zakupu - roznica_vat_prowizji_wyroznienie - prog_pierwszy_vat
            )
            zysk = dochod - roznica_vat

        return CalculationResponse(
            brutto=round(zysk * 1.23, 2),
            na_czysto=round(zysk, 2),
            zysk_procentowy=round((zysk * 100) / cena_netto_zakup, 2),
        ), None, True

    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="calculation_profit",
            type_error="exception",
            key_type_error="Exception",
        ), False
