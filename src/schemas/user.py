from typing import Optional
from pydantic import BaseModel

from .base import BaseInDB


class UserBase(BaseModel):
    username: str
    otp_enabled: Optional[bool] = False
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


class UserCreate(UserBase):
    password: Optional[str] = None
    company_id: Optional[str] = None

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(BaseInDB, UserBase):
    pass

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    secret: str
    otp_secret: Optional[str] = None
    claim_code: Optional[str] = None
    is_claimed: Optional[bool] = False