# fastapi
from fastapi import Depends, status, HTTPException, APIRouter
from fastapi.responses import JSONResponse

# database
from sqlalchemy.orm import Session
from database.list_products.models import ListProducts
from database.db import get_db

# schemas
from routers.list_products.schemas import ListProductsParams, DeleteProduct
from routers.patryk_routers.utilities import check_users_parameters

# jwt
from auth.jwt_handler import check_access_token

router = APIRouter()


@router.get("/routers/list_products/list/get_list")
async def get_list(db: Session = Depends(get_db)):
    try:
        item = db.query(ListProducts).all()
        return item

    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Błąd w sekcji pobierania listy produktów!")


@router.post("/routers/list_products/list/add_products", dependencies=[Depends(check_access_token)])
async def add_products(payload: ListProductsParams, db: Session = Depends(get_db)):
    try:

        response = check_users_parameters({"id": payload.id_user, "username": payload.username, "type_user": True}, db)
        if response is True:
            pass
        elif response["error"]:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": response['error']})

        new_product = ListProducts(name=payload.name, amount=payload.amount, model=payload.model, type=payload.type)
        db.add(new_product)
        db.commit()

        return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "Poprawnie dodano produkt do listy!"})

    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Błąd w sekscji dodawania produktu do listy!")


@router.put("/routers/list_products/list/edit_product", dependencies=[Depends(check_access_token)])
async def edit_product(payload: ListProductsParams, db: Session = Depends(get_db)):
    try:
        response = check_users_parameters({"id": payload.id_user, "username": payload.username, "type_user": True}, db)
        if response is True:
            pass
        elif response["error"]:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": response['error']})

        item_id = db.query(ListProducts).filter(ListProducts.id == payload.id)
        item = item_id.first()
        if not item:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "Brak id produktu!"})

        item.name = payload.name
        item.amount = payload.amount
        item.model = payload.model
        item.type = payload.type

        db.commit()

        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"detail": "Poprawnie przeprowadzono edycje produktu!"})

    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Błąd w sekcji edycji produktu!")


@router.delete("/routers/list_products/list/delete_product", dependencies=[Depends(check_access_token)])
async def delete_product(payload: DeleteProduct, db: Session = Depends(get_db)):
    try:

        response = check_users_parameters({"id": payload.id_user, "username": payload.username, "type_user": True}, db)
        if response is True:
            pass
        elif response["error"]:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": response['error']})

        item_id = db.query(ListProducts).filter(ListProducts.id == payload.id)
        item = item_id.first()
        if not item:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "Brak id produktu!"})

        item_id.delete(synchronize_session=False)
        db.commit()

        return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "Poprawnie usunięto produkt!"})

    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Błąd w sekcji usuwania produktu!")


@router.delete("/routers/list_products/list/delete_all_products", dependencies=[Depends(check_access_token)])
async def delete_all_products(payload: DeleteProduct, db: Session = Depends(get_db)):
    try:
        response = check_users_parameters({"id": payload.id_user, "username": payload.username, "type_user": True}, db)
        if response is True:
            pass
        elif response["error"]:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": response['error']})

        db.query(ListProducts).delete()
        db.commit()

        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"detail": "Poprawnie usunięto całą liste produktów!"})

    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Błąd w sekcji usuwania wszystkich produktów z listy!")
