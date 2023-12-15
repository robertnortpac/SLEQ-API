from app.services.user import UserService
from app.schemas import UserCreate
from app.config import Config
from app.utils.service_result import handle_result

from app.db.base import Base

config = Config()

def init_db(db_session):
    # Create tables
    Base.metadata.create_all(bind=db_session.bind)

    user_in = UserCreate(
        username=config.SUPERUSER_USERNAME,
        password=config.SUPERUSER_USERNAME,
        is_superuser=True,
        otp_enabled=False,
    )
    try:
        handle_result(UserService(db_session).create_user(obj_in=user_in))
    except Exception as e:
        pass