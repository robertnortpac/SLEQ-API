from fastapi import Depends, HTTPException, Security
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from core.auth.jwt import JWTBearer
from db.dependancies import get_db
from schemas import TokenData
from crud.user import CRUDUser
from models.user import User

from config import Config

config = Config()


def get_current_user(
    db: Session = Depends(get_db), token_data: TokenData = Depends(JWTBearer())
):
    user = CRUDUser(db).get(id=token_data.sub)
    if not user:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid user")
    return user


def get_current_active_user(current_user: User = Security(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(current_user: User = Security(get_current_user)):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
