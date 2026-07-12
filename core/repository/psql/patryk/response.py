from dataclasses import dataclass

from database.psql.models.patryk import KeysCalculatorPatryk


@dataclass
class KeysCalculatorResponse:
    id: str
    income_tax: float
    vat: float
    inpost_parcel_locker: float
    inpost_courier: float
    inpost_cash_of_delivery_courier: float
    dpd: float
    allegro_matt: float
    without_smart: float


def _to_keys_calculator_response(model: KeysCalculatorPatryk) -> KeysCalculatorResponse:
    return KeysCalculatorResponse(
        id=str(model.id),
        income_tax=model.income_tax,
        vat=model.vat,
        inpost_parcel_locker=model.inpost_parcel_locker,
        inpost_courier=model.inpost_courier,
        inpost_cash_of_delivery_courier=model.inpost_cash_of_delivery_courier,
        dpd=model.dpd,
        allegro_matt=model.allegro_matt,
        without_smart=model.without_smart,
    )
