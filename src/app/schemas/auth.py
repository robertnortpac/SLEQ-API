from typing import Optional

from pydantic import BaseModel

class Login(BaseModel):
    username: str
    password: str
    otp: Optional[str] = None

class ClaimAccount(BaseModel):
    claim_code: str
    password: str = None
    password_confirm: str = None
    otp: str = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    signature: str
    sub: str
    exp: int