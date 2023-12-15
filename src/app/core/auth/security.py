import pyotp
from passlib.context import CryptContext

from app.config import Config

config = Config()

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password) -> bool:
    return password_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return password_context.hash(password)

def validate_otp(otp: str, secret: str) -> bool:
    totp = pyotp.TOTP(secret)
    return totp.verify(otp)

def show_otp(secret: str) -> str:
    totp = pyotp.TOTP(secret)
    return totp.now()
