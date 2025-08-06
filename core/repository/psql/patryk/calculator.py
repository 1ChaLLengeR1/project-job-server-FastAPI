from core.data.response import ResponseData
from database.db import get_db
from database.database_patryk.models import KeysCalculatorPatryk
from core.data.patryk.calculator.calculator import CalculatorData
from core.utils.patryk.calculator import calculations_calculator, shop_cost
from core.data.user import UserData
from core.repository.psql.user.check import check_user_role_psql


def calculations_psql(user_data: UserData, payload: CalculatorData) -> ResponseData:
    db_gen = get_db()
    db = next(db_gen)
    try:
        check_role = check_user_role_psql(user_data, 'admin')
        if not check_role['is_valid']:
            return ResponseData(
                is_valid=check_role['is_valid'],
                status=check_role['status'],
                data=check_role['data'],
                status_code=check_role['status_code'],
                additional=check_role['additional']
            )

        row_keys = db.query(KeysCalculatorPatryk).first()

        dochodowka = row_keys.income_tax
        vat = row_keys.vat
        roznica_vat_zakupu = payload['gross_purchase'] * vat
        cena_netto_zakup = payload['gross_purchase'] - roznica_vat_zakupu
        roznica_vat_sprzedarz = payload['gross_sales'] * vat
        cena_netto_sprzedarz = payload['gross_sales'] - roznica_vat_sprzedarz
        prowizja_brutto = payload['gross_sales'] * (payload['provision'] / 100)
        wyroznienie_brutto = payload['gross_sales'] * (payload['distinction'] / 100)
        suma_prowizji_wyroznienie = prowizja_brutto + wyroznienie_brutto
        roznica_vat_prowizji_wyroznienie = suma_prowizji_wyroznienie * vat
        prowizja_wyroznienie_netto = suma_prowizji_wyroznienie - roznica_vat_prowizji_wyroznienie

        if payload['gross_sales'] < 40:
            koszt_wysylki = shop_cost(row_keys.id, payload['referrer'], db)
            cena_sprzedarzy_brutto_z_wysylka = payload['gross_sales'] + koszt_wysylki
            cena_sprzedarzy_brutto_z_wysylka_prowizja = cena_sprzedarzy_brutto_z_wysylka * (payload['provision'] / 100)
            roznica_vat_wysylki = cena_sprzedarzy_brutto_z_wysylka_prowizja * vat
            netto_wysylka = cena_sprzedarzy_brutto_z_wysylka_prowizja - roznica_vat_wysylki
            przychod_netto = cena_netto_sprzedarz - cena_netto_zakup - netto_wysylka
            dochodowka_do_zaplacenia = przychod_netto * dochodowka
            dochod = (przychod_netto - dochodowka_do_zaplacenia)
            roznica_vat = roznica_vat_sprzedarz - roznica_vat_zakupu - roznica_vat_wysylki
            zysk = dochod - roznica_vat

            brutto = zysk * 1.23
            na_czysto = zysk
            zysk_procentowy = (zysk * 100) / cena_netto_zakup

            data = {
                "brutto": round(brutto, 2),
                "na_czysto": round(na_czysto, 2),
                "zysk_procentowy": round(zysk_procentowy, 2)
            }

            return ResponseData(
                is_valid=True,
                status="SUCCESS",
                data=data,
                status_code=200,
                additional=None
            )



        elif payload['gross_sales'] >= 40 and payload['gross_sales'] <= 79.99:
            cena_paczki = 0.99

            values_calculations = calculations_calculator(cena_paczki, vat, cena_netto_sprzedarz, cena_netto_zakup,
                                                          prowizja_wyroznienie_netto, dochodowka, roznica_vat_sprzedarz,
                                                          roznica_vat_zakupu, roznica_vat_prowizji_wyroznienie)

            data = {
                "brutto": values_calculations['brutto'],
                "na_czysto": values_calculations['na_czysto'],
                "zysk_procentowy": values_calculations['zysk_procentowy']
            }

            return ResponseData(
                is_valid=True,
                status="SUCCESS",
                data=data,
                status_code=200,
                additional=None
            )

        elif payload['gross_sales'] >= 80 and payload['gross_sales'] <= 199.99:
            cena_paczki = 2.49
            values_calculations = calculations_calculator(cena_paczki, vat, cena_netto_sprzedarz, cena_netto_zakup,
                                                          prowizja_wyroznienie_netto, dochodowka, roznica_vat_sprzedarz,
                                                          roznica_vat_zakupu, roznica_vat_prowizji_wyroznienie)

            data = {
                "brutto": values_calculations['brutto'],
                "na_czysto": values_calculations['na_czysto'],
                "zysk_procentowy": values_calculations['zysk_procentowy']
            }
            return ResponseData(
                is_valid=True,
                status="SUCCESS",
                data=data,
                status_code=200,
                additional=None
            )


        elif payload['gross_sales'] >= 200 and payload['gross_sales'] <= 299.99:
            cena_paczki = 3.99
            values_calculations = calculations_calculator(cena_paczki, vat, cena_netto_sprzedarz, cena_netto_zakup,
                                                          prowizja_wyroznienie_netto, dochodowka, roznica_vat_sprzedarz,
                                                          roznica_vat_zakupu, roznica_vat_prowizji_wyroznienie)

            data = {
                "brutto": values_calculations['brutto'],
                "na_czysto": values_calculations['na_czysto'],
                "zysk_procentowy": values_calculations['zysk_procentowy']
            }

            return ResponseData(
                is_valid=True,
                status="SUCCESS",
                data=data,
                status_code=200,
                additional=None
            )

        elif payload['gross_sales'] >= 300:
            cena_paczki = 4.99
            values_calculations = calculations_calculator(cena_paczki, vat, cena_netto_sprzedarz, cena_netto_zakup,
                                                          prowizja_wyroznienie_netto, dochodowka, roznica_vat_sprzedarz,
                                                          roznica_vat_zakupu, roznica_vat_prowizji_wyroznienie)

            data = {
                "brutto": values_calculations['brutto'],
                "na_czysto": values_calculations['na_czysto'],
                "zysk_procentowy": values_calculations['zysk_procentowy']
            }

            return ResponseData(
                is_valid=True,
                status="SUCCESS",
                data=data,
                status_code=200,
                additional=None
            )




    except Exception as e:
        return ResponseData(
            is_valid=False,
            status="ERROR",
            data=str(e),
            status_code=417,
            additional=None
        )
    finally:
        db.close()
