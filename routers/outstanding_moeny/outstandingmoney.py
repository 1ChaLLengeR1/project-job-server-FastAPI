# fastapi
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.responses import JSONResponse
from datetime import datetime

# database
from database.db import get_db
from sqlalchemy.orm import Session
from database.outstanding_money.models import NamesOverdue, OutStandingMoney

# schemas
from routers.outstanding_moeny.schemas import AddItemParams, EditItem, DeleteId
from routers.patryk_routers.utilities import check_users_parameters

# auth

router = APIRouter()


@router.post("/routers/outstanding_money/outstandingmoney/add_item")
async def add_item(payload: AddItemParams, db: Session = Depends(get_db)):
    try:

        response = check_users_parameters({"id": payload.id_user, "username": payload.username, "type_user": True}, db)
        if response is True:
            pass
        elif response["error"]:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": response['error']})

        find_index = db.query(NamesOverdue).filter(NamesOverdue.id == payload.id_name).first()
        if not find_index:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={"detail": "Brak takiej listy zaległych!"})

        new_item = OutStandingMoney(amount=payload.amount, name=payload.name, date=datetime.now(),
                                    id_name=payload.id_name)
        db.add(new_item)
        db.commit()

        return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "Dodano poprawnie do listy!"})

    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Błąd w sekcji dodawania do listy zaległych!")


@router.put("/routers/outstanding_money/outstandingmoney/edit_item")
async def edit_item(payload: EditItem, db: Session = Depends(get_db)):
    try:
        response = check_users_parameters({"id": payload.id_user, "username": payload.username, "type_user": True}, db)
        if response is True:
            pass
        elif response["error"]:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": response['error']})

        edit_item = db.query(OutStandingMoney).filter(OutStandingMoney.id == payload.id).first()

        if not edit_item:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "Brak id produktu!"})

        edit_item.amount = payload.amount
        edit_item.name = payload.name

        db.commit()

        return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "Poprawnie zmodyfikowano item!"})

    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Błąd w sekcji edycji listy zaległych!")


@router.delete("/routers/outstanding_money/outstandingmoney/delete_item")
async def delete_item(payload: DeleteId, db: Session = Depends(get_db)):
    try:

        response = check_users_parameters({"id": payload.id_user, "username": payload.username, "type_user": True}, db)
        if response is True:
            pass
        elif response["error"]:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": response['error']})

        find_index = db.query(OutStandingMoney).filter(OutStandingMoney.id == payload.id)
        delete_item = find_index.first()

        if not delete_item:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "Brak id produktu!"})

        find_index.delete(synchronize_session=False)
        db.commit()

        return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "Poprawnie usunięto z listy!"})

    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Błąd w sekcji usuwania pozycji w liście zaległych!")
