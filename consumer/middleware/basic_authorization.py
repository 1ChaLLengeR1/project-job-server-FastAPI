import jwt
import datetime
from datetime import datetime, timedelta
from consumer.data.response import ResponseData
from fastapi.security.base import SecurityBase
from consumer.helper.validators import get_env_variable
from database.db import get_db
from database.auth.models import Users
from consumer.middleware.utils import verification_password


class JWTBasicAuthenticationMiddleware(SecurityBase):
    def authenticate(self, request) -> ResponseData:
        try:
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                return ResponseData(
                    is_valid=False,
                    status="ERROR",
                    data=str("You did not provide authorization headers."),
                    status_code=403
                )
            token = auth_header.split(" ")[1]
            err, message = self.decode_jwt(token)
            if err:
                return ResponseData(
                    is_valid=False,
                    status="ERROR",
                    data=str(message),
                    status_code=403
                )
            return ResponseData(
                is_valid=True,
                status="SUCCESS",
                data=None,
                status_code=200
            )

        except IndexError:
            return ResponseData(
                is_valid=False,
                status="ERROR",
                data=str("Bearer token not provided."),
                status_code=403
            )

    def decode_jwt(self, token: str) -> tuple[bool, str]:
        try:
            payload = jwt.decode(
                token,
                get_env_variable("SECRET_KEY_TOKEN"),
                algorithms=[get_env_variable("ALGORITHM")]
            )

            user_id = payload.get("id")
            if not user_id:
                return False, "No such user!"

            return True, ""

        except jwt.ExpiredSignatureError:
            return False, "Token has expired."
        except jwt.DecodeError as e:
            return False, f"Token decode error: {e}"
        except jwt.InvalidTokenError:
            return False, "Invalid token."

    def encode_jwt(self, username: str, password: str, password_on: bool = True) -> tuple[bool, str, dict | None]:
        db_gen = get_db()
        db = next(db_gen)

        try:

            user = db.query(Users).filter(Users.username == username).first()

            if not user:
                return False, f"user not exist with this name: {username}", None

            if password_on:
                if not verification_password(password, user.password):
                    return False, "Password or user name is not correct", None

            expired = datetime.utcnow() + timedelta(
                hours=int(get_env_variable("TOKEN_EXPIRES_HOURS"))
            )

            payload = {
                "id": user.id,
                "exp": expired,
                "iat": datetime.utcnow()
            }

            token = jwt.encode(payload, get_env_variable("SECRET_KEY_TOKEN"), algorithm=get_env_variable("ALGORITHM"))

            data = {
                "id": user.id,
                "username": user.username,
                "access_token": token,
                "refresh_token": self.encode_refresh_jwt(user.id)
            }

            return True, "", data
        except Exception as e:
            return False, str(e), None

    def encode_refresh_jwt(self, user_id: str) -> str:
        token_expires = int(get_env_variable("REFRESH_TOKEN_EXPIRES_HOURS"))
        expires_delta = datetime.utcnow() + timedelta(days=token_expires)
        payload = {
            "id": user_id,
            "exp": expires_delta,
            "iat": datetime.utcnow()
        }
        encode_jwt = jwt.encode(payload, get_env_variable("SECRET_KEY_REFRESH_TOKEN"), get_env_variable("ALGORITHM"))
        return encode_jwt

    def decode_refresh_jwt(self, refresh_token: str, user_id: str) -> tuple[bool, str, dict | None]:
        db_gen = get_db()
        db = next(db_gen)

        try:
            if not refresh_token:
                return False, str("token not provided"), None

            jwt.decode(refresh_token, get_env_variable("SECRET_KEY_REFRESH_TOKEN"), get_env_variable("ALGORITHM"))
            user = db.query(Users).filter(Users.id == user_id).first()

            if not user:
                return False, f"user not exist with this user_id: {user_id}", None

            is_valid, mess, data_user = self.encode_jwt(user.username, user.password, False)
            if not is_valid:
                return False, str(mess), None

            return True, "", data_user
        except Exception as e:
            return False, str(e), None
