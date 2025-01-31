from fastapi import Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime
import time
from jose import jwt, JWTError
from decouple import config

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/authentication/login",
    scheme_name="JWT"
)


def create_access_token(username: str):
    token_expires = int(config("TOKEN_EXPIRES_HOURS"))
    expires_delta = datetime.utcnow() + timedelta(minutes=token_expires)
    to_encode = {"exp": expires_delta, "sub": str(username)}
    encoded_jwt = jwt.encode(to_encode, config("SECRET_KEY_TOKEN"), config("ALGORITHM"))
    return encoded_jwt


def create_refresh_token(username: str):
    token_expires = int(config("REFRESH_TOKEN_EXPIRES_HOURS"))
    expires_delta = datetime.utcnow() + timedelta(days=token_expires)
    to_encode = {"exp": expires_delta, "sub": str(username)}
    encode_jwt = jwt.encode(to_encode, config("SECRET_KEY_REFRESH_TOKEN"), config("ALGORITHM"))
    return encode_jwt


def check_access_token(token: Annotated[str, Depends(reuseable_oauth)]):
    try:
        payload = jwt.decode(token, config("SECRET_KEY_TOKEN"), config("ALGORITHM"))
        username: str = payload.get('sub')
        exp: int = payload.get('exp')

        if not username:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Brak tokenu!",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if datetime.fromtimestamp(exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token wygasł!",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return True


    except(JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Błąd podczas walidacji tokenu!",
            headers={"WWW-Authenticate": "Bearer"},
        )


def check_refresh_token(token: str, user: str):
    try:
        if not token:
            return {"error": "Brak tokenu!"}

        jwt.decode(token, config("SECRET_KEY_REFRESH_TOKEN"), config("ALGORITHM"))
        return {"access_token": create_access_token(user)}
    except(JWTError, ValueError):
        return {"error": "Błąd podczas walidacji tokenu!"}
