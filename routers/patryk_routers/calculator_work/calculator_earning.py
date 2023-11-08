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

        if payload.gross_sales == 0 or payload.gross_purchase == 0:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail":"Zakup i sprzedaż nie mogą być puste oraz nie mogą być zerami!"})


       #Kod jest nie dostępny z przyczyn prywatnych!

    
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
