from passlib.context import CryptContext

from config import Config

config = Config()

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password) -> bool:
    return password_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return password_context.hash(password)
