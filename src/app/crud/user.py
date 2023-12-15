from typing import Optional

from sqlalchemy.orm import Session

from fastapi.encoders import jsonable_encoder

import pyotp

from app.models.user import User
from app.models.company import Company
from app.schemas.user import UserCreate, UserUpdate, UserInDB
from app.core.auth.security import verify_password, get_password_hash
from app.crud.base import CRUDBase



class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def __init__(self, db: Session):
        super().__init__(model=User, db=db)
    def get_by_username(self, *, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    def get_by_claim_code(self, *, claim_code: str) -> Optional[User]:
        return self.db.query(User).filter(User.claim_code == claim_code).first()

    def authenticate(
        self, *, username: str, password: str, otp: str = None
    ) -> Optional[User]:
        user = self.get_by_username(username=username)
        if not user:
            return None
        if not verify_password(password, user.secret):
            return None
        return user

    def validate_otp(self, user: User, otp: str) -> bool:
        if user.otp_enabled:
            if user.is_claimed:
                totp = pyotp.TOTP(user.otp_secret)
                if not totp.verify(otp):
                    return False
            else:
                return False
        return True

    def provision_otp(self, user: User) -> str:
        if user.otp_enabled:
            totp = pyotp.TOTP(user.otp_secret)
            return totp.provisioning_uri(user.username, issuer_name="SLEQ API")
        return None

    def is_claimed(self, user: User) -> bool:
        return user.is_claimed

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser
    
    def is_uniquely_named(self, user_in: User, obj_in: UserUpdate) -> bool:
        user = self.get_by_username(username=obj_in.username)
        if not user:
            return True
        if user.id == user_in.id:
            return True
        return False
    
