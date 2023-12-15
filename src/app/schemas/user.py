from typing import Optional
from pydantic import BaseModel

from .base import BaseInDB


class UserBase(BaseModel):
    username: Optional[str] = None
    otp_enabled: Optional[bool] = False
    is_superuser: Optional[bool] = False
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    username: str
    otp_enabled: bool
    is_superuser: bool
    password: str
    company_id: Optional[str] = None

class UserUpdate(UserBase):
    is_superuser: Optional[bool] = False
    is_active: Optional[bool] = True

class UserInDBBase(BaseInDB, UserBase):
    pass

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    secret: str
    otp_secret: Optional[str] = None
    claim_code: Optional[str] = None
    is_claimed: Optional[bool] = False