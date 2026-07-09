import uuid
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from config.settings import settings
from core.data.user import UserData
from core.middleware.utils import verification_password
from core.repository.psql.user.one import one_user_by_id_psql
from database.psql.database import get_db
from database.psql.models.auth import Users


class JWTBasicAuthenticationMiddleware(HTTPBearer):
    """Dependency FastAPI (nie klasyczne ASGI middleware).

    Przepływ: Bearer token → dekodowanie JWT → claim `id` walidowany jako UUID →
    pobranie usera z DB → weryfikacja roli względem `roles` → zwrot danych usera.

    - `roles=None` — wystarczy poprawny token (każdy zalogowany user),
    - `roles=["admin"]` — wpuszcza admina (i superadmina — superadmin przechodzi każdy check),
    - 401 — problem z tokenem, 403 — brak uprawnień.
    """

    def __init__(self, roles: list[str] | None = None, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
        self.roles = roles

    async def __call__(self, request: Request) -> UserData:
        try:
            credentials: HTTPAuthorizationCredentials | None = await super().__call__(request)
        except HTTPException as err:
            raise HTTPException(status_code=401, detail=err.detail) from err

        if not credentials or credentials.scheme != "Bearer":
            raise HTTPException(status_code=401, detail="Bearer token not provided.")

        is_valid, message, user_id = self.decode_jwt(credentials.credentials)
        if not is_valid:
            raise HTTPException(status_code=401, detail=message)

        user, _, ok = one_user_by_id_psql(user_id)
        if not ok or user is None:
            raise HTTPException(status_code=401, detail="User from token does not exist.")

        if self.roles and user.type != "superadmin" and user.type not in self.roles:
            raise HTTPException(status_code=403, detail=f"User '{user.username}' has no permission.")

        return UserData(id=user.id, username=user.username, type=user.type)

    def decode_jwt(self, token: str) -> tuple[bool, str, str | None]:
        try:
            payload = jwt.decode(token, settings.secret_key_token, algorithms=[settings.algorithm])

            user_id = payload.get("id")
            if not user_id:
                return False, "Token has no 'id' claim.", None

            try:
                uuid.UUID(str(user_id))
            except ValueError:
                return False, "Claim 'id' is not a valid UUID.", None

            return True, "", str(user_id)

        except jwt.ExpiredSignatureError:
            return False, "Token has expired.", None
        except jwt.DecodeError as e:
            return False, f"Token decode error: {e}", None
        except jwt.InvalidTokenError:
            return False, "Invalid token.", None

    def encode_jwt(self, username: str, password: str, password_on: bool = True) -> tuple[bool, str, dict | None]:
        db_gen = get_db()
        db = next(db_gen)

        try:
            user = db.query(Users).filter(Users.username == username).first()
            if not user:
                return False, f"user not exist with this name: {username}", None

            if password_on and not verification_password(password, user.password):
                return False, "Password or user name is not correct", None

            expired = datetime.now(timezone.utc) + timedelta(hours=settings.token_expires_hours)

            payload = {"id": str(user.id), "exp": expired, "iat": datetime.now(timezone.utc)}

            token = jwt.encode(payload, settings.secret_key_token, algorithm=settings.algorithm)

            data = {
                "id": str(user.id),
                "username": user.username,
                "access_token": token,
                "refresh_token": self.encode_refresh_jwt(str(user.id)),
            }

            return True, "", data
        except Exception as e:
            return False, str(e), None

    def encode_refresh_jwt(self, user_id: str) -> str:
        token_expires = settings.refresh_token_expires_hours
        expires_delta = datetime.now(timezone.utc) + timedelta(days=token_expires)
        payload = {"id": user_id, "exp": expires_delta, "iat": datetime.now(timezone.utc)}
        encode_jwt = jwt.encode(payload, settings.secret_key_refresh_token, settings.algorithm)
        return encode_jwt

    def decode_refresh_jwt(self, refresh_token: str, user_id: str) -> tuple[bool, str, dict | None]:
        db_gen = get_db()
        db = next(db_gen)

        try:
            if not refresh_token:
                return False, "token not provided", None

            jwt.decode(refresh_token, settings.secret_key_refresh_token, settings.algorithm)
            user = db.query(Users).filter(Users.id == user_id).first()

            if not user:
                return False, f"user not exist with this user_id: {user_id}", None

            is_valid, mess, data_user = self.encode_jwt(user.username, user.password, False)
            if not is_valid:
                return False, str(mess), None

            return True, "", data_user
        except Exception as e:
            return False, str(e), None
