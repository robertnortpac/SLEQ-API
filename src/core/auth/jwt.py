from datetime import datetime, timedelta

from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from starlette.status import HTTP_403_FORBIDDEN

from config import Config
from models.user import User
from schemas import TokenData


config = Config()


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, Request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(Request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail="Invalid authentication scheme.",
                )
            payload = self.decode_jwt(credentials.credentials)
            if not payload:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail="Invalid token or expired token.",
                )
            if not self.verify_payload(payload):
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail="Token signature is invalid.",
                )
            return TokenData(**payload)
        else:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Invalid authorization code."
            )

    def verify_payload(self, payload: dict) -> bool:
        try:
            if payload["signature"] != config.TOKEN_SIGNATURE:
                return False
            return True
        except JWTError:
            return False
        
    def decode_jwt(self, jwtoken: str) -> dict:
        try:
            payload = jwt.decode(
                jwtoken, config.SECRET_KEY, algorithms=[config.ALGORITHM]
            )
            return payload
        except JWTError:
            return False


def create_access_token(user: User, expires_delta: timedelta | None = None):
    to_encode = dict()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update(
        {"exp": expire, "signature": config.TOKEN_SIGNATURE, "sub": str(user.id)}
    )
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt
