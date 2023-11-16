from fastapi import Depends, status, HTTPException, APIRouter
# fastapi response
from fastapi.responses import JSONResponse
# schemas
from routers.house_settlement_moeny.basic_rental_values.schemas import BasicRental
from routers.patryk_routers.utilities import check_users_parameters
# database
from sqlalchemy.orm import Session
from database.house_settlement_money.basic_rental_values.models import BasicRentalValues
from database.db import get_db
# jwt
from auth.jwt_handler import check_access_token

router = APIRouter()


@router.get('/routers/house_settlement_money/basic_rental_values/basic_values/get_values')
async def get_values(db: Session = Depends(get_db)):
    try:
        return db.query(BasicRentalValues).all()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Błąd w sekcji pobierania podstawowych wartościu czynszu!")


@router.put("/routers/house_settlement_money/basic_rental_values/basic_values/edit_values",
            dependencies=[Depends(check_access_token)])
async def edit_values(payload: BasicRental, db: Session = Depends(get_db)):
    try:
        response = check_users_parameters({"id": payload.id_user, "username": payload.username, "type_user": True}, db)
        if response is True:
            pass
        elif response["error"]:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": response['error']})

        item_id = db.query(BasicRentalValues).filter(BasicRentalValues.id == payload.id).first()
        if not item_id:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail":"Brak id wartości wynajmującego!"})

        item_id.electric_current = payload.electric_current
        item_id.water = payload.water
        item_id.transfer = payload.transfer
        item_id.trash = payload.trash
        item_id.internet = payload.internet

        db.commit()

        return JSONResponse(status_code=status.HTTP_200_OK, content={"detail":"Poprawnie przeprowadzono edycje wartości wynajmującego!"})

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Błąd w sekcji edytowania wartości czynszu!")
