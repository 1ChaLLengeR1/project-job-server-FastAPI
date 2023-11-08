from database.auth.models import Users
from database.database_patryk.models import KeysCalculatorPatryk
from pydantic import BaseModel


class User(BaseModel):
    id: str
    username: str
    type_user: bool


def check_users_parameters(user: User, db):
    user_id = db.query(Users).filter(Users.id == user["id"]).first()
    if not user_id:
        return {"error": "Brak takiego id użytkownika!!"}
    if user_id.username != user["username"]:
        return {"error": "Brak takiego użytkownika!"}
    if user["type_user"]:
        if user_id.type != 'superadmin':
            return {"error": "Brak uprawnieni do wykoanania tej metody!"}

    return True


def shop_cost(user_id: str or int, referrer: str, db):
    keys_id_price = db.query(KeysCalculatorPatryk).with_entities(KeysCalculatorPatryk.inpost_parcel_locker,
                                                                 KeysCalculatorPatryk.inpost_courier,
                                                                 KeysCalculatorPatryk.inpost_cash_of_delivery_courier,
                                                                 KeysCalculatorPatryk.dpd,
                                                                 KeysCalculatorPatryk.allegro_matt,
                                                                 KeysCalculatorPatryk.without_smart).filter(
        KeysCalculatorPatryk.id == user_id).first()

    if referrer == 'inpost_parcel_locker':
        return keys_id_price.inpost_parcel_locker
    if referrer == 'inpost_courier':
        return keys_id_price.inpost_courier
    if referrer == 'inpost_cash_of_delivery_courier':
        return keys_id_price.inpost_cash_of_delivery_courier
    if referrer == 'dpd':
        return keys_id_price.dpd
    if referrer == 'allegro_matt':
        return keys_id_price.allegro_matt
    if referrer == 'without_smart':
        return keys_id_price.without_smart
    else:
        return 0


def calculations_calculator(package_price: float, vat: float, cena_netto_sprzedarz: float, cena_netto_zakup: float,
                 prowizja_wyroznienie_netto: float, dochodowka: float, roznica_vat_sprzedarz: float,
                 roznica_vat_zakupu: float, roznica_vat_prowizji_wyroznienie: float):
                     
    #Kod jest nie dostępny z przyczyn prywatnych!

    return {
        "brutto": round(brutto, 2),
        "na_czysto": round(na_czysto, 2),
        "zysk_procentowy": round(zysk_procentowy, 2)
    }
