import json
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from auth.schemas import LoginUserSchema, RefreshTokenSchema
from database.db import get_db
from database.auth.models import Users
from auth.utilities import verification_password
from auth.jwt_handler import create_access_token, create_refresh_token, check_refresh_token

router = APIRouter()


@router.post('/authentication/login')
async def login(payload: LoginUserSchema, db: Session = Depends(get_db)):
    try:
        user_id = db.query(Users).filter(Users.username == payload.username).first()
        if not user_id:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                                content={"detail": "Brak takiego użytkownika!"})

        if not verification_password(payload.password, user_id.password):
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                                content={"detail": "Nieprawidłowe dane logowania!"})

        return {
            "id": user_id.id,
            "username": user_id.username,
            "access_token": create_access_token(user_id),
            "refresh_token": create_refresh_token(user_id)
        }

    except HTTPException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Błąd w sekcji logowanie!")


@router.post('/authentication/automatically-login')
async def automatically_login(payload: RefreshTokenSchema, db: Session = Depends(get_db)):
    try:
        user_id = db.query(Users).filter(Users.id == payload.id).first()
        if not user_id:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                                content={"detail": "Niepoprawne id użytkownika!"})

        token = json.dumps(check_refresh_token(payload.refresh_token, user_id))
        response = json.loads(token)

        try:
            if response["error"]:
                return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": response["error"]})

        except:
            return {
                "id": user_id.id,
                "username": user_id.username,
                "access_token": create_access_token(user_id),
                "refresh_token": create_refresh_token(user_id)
            }



    except HTTPException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Błąd w sekcji refresh token!")
