from crud.user import CRUDUser
from schemas import UserCreate
from config import Config

from db.base import Base

config = Config()

def init_db(db_session):
    # Create tables
    Base.metadata.create_all(bind=db_session.bind)

    user = CRUDUser(db_session).get_by_username(username=config.SUPERUSER_USERNAME)
    if not user:
        user_in = UserCreate(
            username=config.SUPERUSER_USERNAME,
            password=config.SUPERUSER_USERNAME,
            is_superuser=True
        )
        user = CRUDUser(db_session).create(obj_in=user_in)