from typing import Optional

from sqlalchemy.orm import Session

import pyotp

from models.user import User
from models.company import Company
from schemas.user import UserCreate, UserUpdate, UserInDB
from core.auth.security import verify_password, get_password_hash
from crud.base import CRUDBase
from utils.generator import generate_claim_code, generate_random_password


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def __init__(self, db: Session):
        super().__init__(model=User, db=db)
    def get_by_username(self, *, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    def get_by_claim_code(self, *, claim_code: str) -> Optional[User]:
        return self.db.query(User).filter(User.claim_code == claim_code).first()

    def create(
        self, *, obj_in: UserCreate, company: Company = None, current_user: User = None
    ) -> User:
        if not obj_in.password:
            obj_in.password = generate_random_password()
        db_obj = User(
            username=obj_in.username,
            secret=get_password_hash(obj_in.password),
            otp_enabled=obj_in.otp_enabled,
            is_superuser=obj_in.is_superuser,
        )
        if obj_in.otp_enabled:
            db_obj.otp_secret = pyotp.random_base32()
            db_obj.claim_code = generate_claim_code()
        if current_user:
            setattr(db_obj, "created_by", current_user.id)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        if company:
            company.users.append(db_obj)
            db_obj.current_company_id = company.id
            self.db.commit()
            self.db.refresh(company)
        return db_obj

    def update(
        self, *, db_obj: User, obj_in: UserUpdate, current_user: User = None
    ) -> User:
        update_data = obj_in.model_dump(exclude_unset=True)
        if obj_in.password:
            hashed_password = get_password_hash(obj_in.password)
            del update_data["password"]
            update_data["secret"] = hashed_password
        use_obj_in = UserInDB.model_validate(update_data)
        return super().update(
            db_obj=db_obj, obj_in=use_obj_in, current_user=current_user
        )

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
