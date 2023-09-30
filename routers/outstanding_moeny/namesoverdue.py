# fastapi
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.responses import JSONResponse
import uuid
from datetime import datetime

# database
from database.db import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database.outstanding_money.models import NamesOverdue, OutStandingMoney

# schemas
from routers.outstanding_moeny.schemas import CreateListParams, EditListParams, DeleteId
from routers.patryk_routers.utilities import check_users_parameters

# import auth
from auth.jwt_handler import check_access_token

router = APIRouter()


@router.get("/routers/outstanding_money/names_overdue/get_list")
async def get_list(db: Session = Depends(get_db)):
    try:

        list_overdue = []
        item_names_overdue = db.query(NamesOverdue).all()

        for item in item_names_overdue:
            object_item = {
                "id_name": item.id,
                "name_overdue": item.name,
                "array_items": [],
                "full_price": 0
            }

            item_outstanding_money = db.query(OutStandingMoney).filter(OutStandingMoney.id_name == item.id).all()
            for items in item_outstanding_money:
                object_items = {
                    "id": items.id,
                    "amount": items.amount,
                    "name": items.name,
                    "date": items.date,
                }
                object_item['array_items'].append(object_items)
                object_item['full_price'] = object_item['full_price'] + items.amount

            list_overdue.append(object_item)

        return list_overdue
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Błąd w sekcji pobierania listy zaległych")


@router.post("/routers/outstanding_money/names_overdue/create_list", dependencies=[Depends(check_access_token)])
async def create_list(payload: CreateListParams, db: Session = Depends(get_db)):
    try:

        response = check_users_parameters({"id": payload.id_user, "username": payload.username, "type_user": True}, db)
        if response is True:
            pass
        elif response["error"]:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": response['error']})

        new_uuid4 = uuid.uuid4()

        new_names_overdue = NamesOverdue(id=new_uuid4, name=payload.name)
        db.add(new_names_overdue)

        for item in payload.array_object:
            new_outstanding_money = OutStandingMoney(amount=item['amount'], name=item['name'], date=datetime.now(),
                                                     id_name=new_uuid4)
            db.add(new_outstanding_money)

        db.commit()
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"detail": "Poprawnie dodano nową listę zaległych!"})

    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Błąd w skecji dodawania zaległej listy!")


@router.put("/routers/outstanding_money/names_overdue/edit_name_list", dependencies=[Depends(check_access_token)])
async def edit_name_list(payload: EditListParams, db: Session = Depends(get_db)):
    try:

        response = check_users_parameters({"id": payload.id_user, "username": payload.username, "type_user": True}, db)
        if response is True:
            pass
        elif response["error"]:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": response['error']})

        item_id = db.query(NamesOverdue).filter(NamesOverdue.id == payload.id).first()
        if not item_id:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "Brak id zaległej listy!"})

        item_id.name = payload.name
        db.commit()
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"detail": "Poprawnie z modyfikowano nazwę listy zaległych!"})
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Błąd w sekcji edycji nazyw listy zaległych!")


@router.delete("/routers/outstanding_money/names_overdue/delete_list", dependencies=[Depends(check_access_token)])
async def delete_list(payload: DeleteId, db: Session = Depends(get_db)):
    try:
        response = check_users_parameters({"id": payload.id_user, "username": payload.username, "type_user": True}, db)
        if response is True:
            pass
        elif response["error"]:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": response['error']})

        item_names_overdue = db.query(NamesOverdue).filter(NamesOverdue.id == payload.id).delete()

        if not item_names_overdue:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "Brak id nazwy zaległego"})

        item_outstanding_money = db.query(OutStandingMoney).filter(OutStandingMoney.id_name == payload.id).delete()

        if not item_outstanding_money:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "Brak id listy zaległych!"})

        db.commit()

        return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "Poprawnie usunięto liste zaległych!"})

    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Błąd w sekscji usuwanie listy zaległych!")
