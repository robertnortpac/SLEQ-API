from dotenv import load_dotenv
import os
from utils.generator import generate_random_signature

load_dotenv()

class Config:
    # Security
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    ALGORITHM: str = "HS256"
    TOKEN_SIGNATURE: str = os.getenv('TOKEN_SIGNATURE')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

    # Super user
    SUPERUSER_USERNAME: str = os.getenv('SUPERUSER_USERNAME')
    SUPERUSER_PASSWORD: str = os.getenv('SUPERUSER_PASSWORD')

    MYSQL_URI: str = os.getenv('MYSQL_URI')
    DEFAULT_TAKE: int = os.getenv('DEFAULT_TAKE')