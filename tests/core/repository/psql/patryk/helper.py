from sqlalchemy.orm import Session

from database.psql.models.patryk import KeysCalculatorPatryk


def make_calculator_keys(
    db: Session,
    *,
    income_tax: float = 0.12,
    vat: float = 0.23,
    inpost_parcel_locker: float = 12.99,
    inpost_courier: float = 15.99,
    inpost_cash_of_delivery_courier: float = 19.99,
    dpd: float = 14.99,
    allegro_matt: float = 9.99,
    without_smart: float = 11.99,
) -> KeysCalculatorPatryk:
    keys = KeysCalculatorPatryk(
        income_tax=income_tax,
        vat=vat,
        inpost_parcel_locker=inpost_parcel_locker,
        inpost_courier=inpost_courier,
        inpost_cash_of_delivery_courier=inpost_cash_of_delivery_courier,
        dpd=dpd,
        allegro_matt=allegro_matt,
        without_smart=without_smart,
    )
    db.add(keys)
    db.flush()
    return keys
