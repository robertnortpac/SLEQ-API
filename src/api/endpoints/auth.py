from datetime import timedelta

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.param_functions import Form
from sqlalchemy.orm import Session

import qrcode
from qrcode.image.svg import SvgImage
from lxml import etree

from crud.user import CRUDUser
from models.user import User
from db.dependancies import get_db
from core.auth.jwt import create_access_token
from schemas import Token, TokenData
from schemas.user import UserUpdate
from schemas.auth import ClaimAccount, Login
from config import Config

config = Config()

router = APIRouter()


@router.post("/login", response_model=Token)
def login_access_token(
    login_data: Annotated[Login, Body(...)],
    db: Session = Depends(get_db),
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = CRUDUser(db).authenticate(
        username=login_data.username, password=login_data.password, otp=login_data.otp
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    elif not CRUDUser(db).validate_otp(user, login_data.otp):
        raise HTTPException(status_code=400, detail="Invalid OTP")
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user=user, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

# @router.get("/claim/{claim_code}")
# def get_claim_code(
#     *,
#     db: Session = Depends(get_db),
#     claim_code: str,
# ):
#     """
#     Get a claim code for an unclaimed account
#     """
#     user = crud.user.get_by_claim_code(db, claim_code=claim_code)
#     if not user:
#         raise HTTPException(status_code=400, detail="Invalid claim code")
#     if user.is_claimed:
#         raise HTTPException(status_code=400, detail="Account already claimed")
#     img = qrcode.make(crud.user.provision_otp(user), image_factory=SvgImage)
#     svg = etree.tostring(img.get_image())
#     return Response(svg, media_type="image/svg+xml")


# @router.post("/claim/{claim_code}")
# def claim_account(
#     *,
#     db: Session = Depends(get_db),
#     claim_code: str,
#     claim_data: Annotated[ClaimAccount, Body(...)],
# ):
#     """
#     Claim an account using a claim code
#     """
#     user = crud.user.get_by_claim_code(db, claim_code=claim_code)
#     if not user:
#         raise HTTPException(status_code=400, detail="Invalid claim code")
#     if user.is_claimed:
#         raise HTTPException(status_code=400, detail="Account already claimed")
#     if claim_data.password != claim_data.password_confirm:
#         raise HTTPException(status_code=400, detail="Passwords do not match")

#     user.is_claimed = True
#     if not crud.user.validate_otp(user, claim_data.otp):
#         raise HTTPException(status_code=400, detail="Invalid OTP")
#     obj_in = UserUpdate(
#         password=claim_data.password,
#         username=user.username,
#         is_active=user.is_active,
#         is_superuser=user.is_superuser,
#         is_claimed=user.is_claimed,
#     )
#     user = crud.user.update(db, db_obj=user, obj_in=obj_in, current_user=user)
#     return {}
