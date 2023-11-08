from fastapi import Depends, status, HTTPException, APIRouter
# fastapi response
from fastapi.responses import JSONResponse
# schemas
from routers.house_settlement_moeny.flats.schemas import FlatsParams
from routers.patryk_routers.utilities import check_users_parameters
# database
from sqlalchemy.orm import Session
from database.house_settlement_money.flats.models import ListFlats
from database.db import get_db
# jwt
from auth.jwt_handler import check_access_token

router = APIRouter()


@router.get("/routers/house_settlement_money/flats/flats/get_flats")
async def get_flats(db: Session = Depends(get_db)):
    try:
        return db.query(ListFlats).all()
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Błąd w trkacie pobierania listy mieszkań!")


@router.post("/routers/house_settlement_money/flats/flats/add_flats", dependencies=[Depends(check_access_token)])
async def add_flats(payload: FlatsParams, db: Session = Depends(get_db)):
    try:

        response = check_users_parameters({"id": payload.id_user, "username": payload.username, "type_user": True}, db)
        if response is True:
            pass
        elif response["error"]:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": response['error']})

        new_flat = ListFlats(house_name=payload.house_name, professional_house_name=payload.professional_house_name)
        db.add(new_flat)
        db.commit()

        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content={"detail": "Poprawnie dodano pokój!"})
    except():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Błąd w sekcji dodawania mieszkania!")


@router.put("/routers/house_settlement_money/flats/flats/edit_flat", dependencies=[Depends(check_access_token)])
async def edit_flats(payload: FlatsParams, db: Session = Depends(get_db)):
    try:
        response = check_users_parameters({"id": payload.id_user, "username": payload.username, "type_user": True}, db)
        if response is True:
            pass
        elif response["error"]:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": response['error']})

        item_id = db.query(ListFlats).filter(ListFlats.id == payload.id)
        item = item_id.first()
        if not item:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "Brak id pokoju!"})

        item.house_name = payload.house_name
        item.professional_house_name = payload.professional_house_name

        db.commit()

        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"detail": "Poprawnie przeprowadzono edycje pokoju!"})


    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Błąd w skecji edytowania mieszkania!")


@router.delete("/routers/house_settlement_money/flats/flats/delete_flat", dependencies=[Depends(check_access_token)])
async def delete_flat(payload: FlatsParams, db: Session = Depends(get_db)):
    try:
        response = check_users_parameters({"id": payload.id_user, "username": payload.username, "type_user": True}, db)
        if response is True:
            pass
        elif response["error"]:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": response['error']})

        item_id = db.query(ListFlats).filter(ListFlats.id == payload.id)
        if not item_id:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "Brak id pokoju!"})

        item_id.delete(synchronize_session=False)
        db.commit()

        return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "Poprawnie usunięto pokój!"})

    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Błąd w sekcji usuwania pokoju!")
