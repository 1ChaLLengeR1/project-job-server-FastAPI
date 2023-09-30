from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from database.database_patryk.models import KeysCalculatorPatryk
from sqlalchemy.orm import Session
from database.db import get_db
from routers.patryk_routers.utilities import check_users_parameters, shop_cost, calculations_calculator
from routers.patryk_routers.calculator_work.schemas import CalculatorParams, KeysCalculator

router = APIRouter()


@router.get("/routes/patryk_routers/calculator_work/calculator_earning/keys_calculator_values")
async def keys_calculator_values(db: Session = Depends(get_db)):
    try:
        return db.query(KeysCalculatorPatryk).first()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Błąd podczas pobierania kluczy kalkulatora!")

@router.post("/routers/patryk_routers/calculator_work/calculator_earning/calculations")
async def calculations(payload: CalculatorParams, db: Session = Depends(get_db)):
    try:
        response = check_users_parameters({"id": payload.id, "username": payload.username, "type_user": False}, db)
        if response is True:
            pass
        elif response["error"]:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": response['error']})

        keys_id = db.query(KeysCalculatorPatryk).first()

        # values
        dochodowka = keys_id.income_tax
        vat = keys_id.vat
        roznica_vat_zakupu = payload.gross_purchase * vat
        cena_netto_zakup = payload.gross_purchase - roznica_vat_zakupu
        roznica_vat_sprzedarz = payload.gross_sales * vat
        cena_netto_sprzedarz = payload.gross_sales - roznica_vat_sprzedarz
        prowizja_brutto = payload.gross_sales * (payload.provision / 100)
        wyroznienie_brutto = payload.gross_sales * (payload.distinction / 100)
        suma_prowizji_wyroznienie = prowizja_brutto + wyroznienie_brutto
        roznica_vat_prowizji_wyroznienie = suma_prowizji_wyroznienie * vat
        prowizja_wyroznienie_netto = suma_prowizji_wyroznienie - roznica_vat_prowizji_wyroznienie

        if payload.gross_sales < 40:
            koszt_wysylki = shop_cost(keys_id.id, payload.referrer, db)
            cena_sprzedarzy_brutto_z_wysylka = payload.gross_sales + koszt_wysylki
            cena_sprzedarzy_brutto_z_wysylka_prowizja = cena_sprzedarzy_brutto_z_wysylka * (payload.provision / 100)
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

            return {
                "brutto": round(brutto, 2),
                "na_czysto": round(na_czysto, 2),
                "zysk_procentowy": round(zysk_procentowy, 2)
            }
        elif payload.gross_sales >= 40 and payload.gross_sales <= 79.99:
            cena_paczki = 0.99

            values_calculations = calculations_calculator(cena_paczki, vat, cena_netto_sprzedarz, cena_netto_zakup,
                                                          prowizja_wyroznienie_netto, dochodowka, roznica_vat_sprzedarz,
                                                          roznica_vat_zakupu, roznica_vat_prowizji_wyroznienie)

            return {
                "brutto": values_calculations['brutto'],
                "na_czysto": values_calculations['na_czysto'],
                "zysk_procentowy": values_calculations['zysk_procentowy']
            }

        elif payload.gross_sales >= 80 and payload.gross_sales <= 199.99:
            cena_paczki = 2.49
            values_calculations = calculations_calculator(cena_paczki, vat, cena_netto_sprzedarz, cena_netto_zakup,
                                                          prowizja_wyroznienie_netto, dochodowka, roznica_vat_sprzedarz,
                                                          roznica_vat_zakupu, roznica_vat_prowizji_wyroznienie)

            return {
                "brutto": values_calculations['brutto'],
                "na_czysto": values_calculations['na_czysto'],
                "zysk_procentowy": values_calculations['zysk_procentowy']
            }
        elif payload.gross_sales >= 200 and payload.gross_sales <= 299.99:
            cena_paczki = 3.99
            values_calculations = calculations_calculator(cena_paczki, vat, cena_netto_sprzedarz, cena_netto_zakup,
                                                          prowizja_wyroznienie_netto, dochodowka, roznica_vat_sprzedarz,
                                                          roznica_vat_zakupu, roznica_vat_prowizji_wyroznienie)

            return {
                "brutto": values_calculations['brutto'],
                "na_czysto": values_calculations['na_czysto'],
                "zysk_procentowy": values_calculations['zysk_procentowy']
            }
        elif payload.gross_sales >= 300:
            cena_paczki = 4.99
            values_calculations = calculations_calculator(cena_paczki, vat, cena_netto_sprzedarz, cena_netto_zakup,
                                                          prowizja_wyroznienie_netto, dochodowka, roznica_vat_sprzedarz,
                                                          roznica_vat_zakupu, roznica_vat_prowizji_wyroznienie)

            return {
                "brutto": values_calculations['brutto'],
                "na_czysto": values_calculations['na_czysto'],
                "zysk_procentowy": values_calculations['zysk_procentowy']
            }
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Błąd w sekcji kalkulator!")


@router.put("/routes/patryk_routers/calculator_work/calculator_earning/keys_calculator_edit")
async def keys_calculator_edit(payload: KeysCalculator, db: Session = Depends(get_db)):
    try:

        response = check_users_parameters({"id": payload.id_user, "username": payload.username, "type_user": False}, db)
        if response is True:
            pass
        elif response["error"]:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": response['error']})

        keys_id = db.query(KeysCalculatorPatryk).filter(KeysCalculatorPatryk.id == payload.id).first()

        if not keys_id:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail":"Brak takiego id!"})


        keys_id.income_tax = payload.income_tax
        keys_id.vat = payload.vat
        keys_id.inpost_parcel_locker = payload.inpost_parcel_locker
        keys_id.inpost_courier = payload.inpost_courier
        keys_id.inpost_cash_of_delivery_courier = payload.inpost_cash_of_delivery_courier
        keys_id.dpd = payload.dpd
        keys_id.allegro_matt = payload.allegro_matt
        keys_id.without_smart = payload.without_smart

        db.commit()

        return JSONResponse(status_code=status.HTTP_200_OK, content={"detail":"Poprawnie przeprowadzono edycje!"})
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Błąd w sekcji edytowania zawartości kalkulatora!")
