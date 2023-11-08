from fastapi import Depends, status, HTTPException, APIRouter
# fastapi response
from fastapi.responses import JSONResponse
# schemas
from routers.house_settlement_moeny.flats.schemas import AddFlatsParams
from routers.patryk_routers.utilities import check_users_parameters
#database
from sqlalchemy.orm import Session
from database.house_settlement_money.flats.models import ListProducts
from database.db import get_db
# jwt
from auth.jwt_handler import check_access_token

router = APIRouter()

@router.post("/routers/house_settlement_money/flats/flats/add_flats", dependencies=[Depends(check_access_token)])
async def add_flats(payload: AddFlatsParams, db: Session = Depends(get_db)):
    try:

        response = check_users_parameters({"id": payload.id_user, "username": payload.username, "type_user": True}, db)
        if response is True:
            pass
        elif response["error"]:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": response['error']})

        new_flat = ListProducts(house_name=payload.house_name, professional_house_name=payload.professional_house_name)
        db.add(new_flat)
        db.commit()

        return JSONResponse(status_code=201, content={"detail": "Poprawnie dodano produkt do listy!"})
    except():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Błąd w sekcji dodawania mieszkania!")

