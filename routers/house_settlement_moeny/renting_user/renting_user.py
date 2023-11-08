from fastapi import Depends, status, HTTPException, APIRouter
# fastapi response
from fastapi.responses import JSONResponse
# schemas
from routers.patryk_routers.utilities import check_users_parameters
from routers.house_settlement_moeny.renting_user.schemas import RentingUser
# database
from sqlalchemy.orm import Session
from database.house_settlement_money.renting_user.modules import Renting
from database.house_settlement_money.flats.models import Flats
from database.db import get_db
# jwt
from auth.jwt_handler import check_access_token

router = APIRouter()


@router.get("/routers/house_settlement_money/renting_user/renting_user/get_users")
async def get_users(db: Session = Depends(get_db)):
    try:
        return db.query(Renting).all()
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Błąd w skecji pobierania wynajmujących!")


@router.post("/routers/house_settlement_money/renting_user/renting_user/add_user",
             dependencies=[Depends(check_access_token)])
async def add_user(payload: RentingUser, db: Session = Depends(get_db)):
    try:

        response = check_users_parameters({"id": payload.id_user, "username": payload.username, "type_user": True}, db)
        if response is True:
            pass
        elif response["error"]:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": response['error']})

        id_item_flats = db.query(Flats).filter(Flats.id == payload.id_flats)
        item = id_item_flats.first()
        if not item:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail":"Brak takiego pokoju!"})

        new_item = Renting(name=payload.name, quantity_users=payload.quantity_users, name_flats=item.professional_house_name,
                           id_flats=payload.id_flats)
        db.add(new_item)
        db.commit()
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content={"detail": "Poprawnie dodano nowego wynajmującego!"})

    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Błąd w sekcji tworzenia wynajmującego!")
