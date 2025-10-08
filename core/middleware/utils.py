from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verification_password(password: str, hash_password: str):
    return pwd_context.verify(password, hash_password)
