from typing import Annotated

from fastapi import APIRouter, Depends, Body, Response
from fastapi.param_functions import Form
from sqlalchemy.orm import Session

from app.db.dependancies import get_db
from app.utils.service_result import handle_result

from app.schemas.auth import Token
from app.schemas.user import User as UserSchema
from app.schemas.auth import ClaimAccount, Login
from app.services.auth import AuthenticationService

router = APIRouter()

@router.post("/login", response_model=Token)
def login_access_token(
    login_data: Annotated[Login, Body(...)],
    db: Session = Depends(get_db),
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    result = AuthenticationService(db).authenticate_user(obj_in=login_data)
    return handle_result(result)


@router.get("/claim/{claim_code}")
def get_claim_code(
    *,
    db: Session = Depends(get_db),
    claim_code: str,
):
    """
    Get a claim code for an unclaimed account
    """
    result = AuthenticationService(db).generate_qr_by_claim_code(claim_code=claim_code)
    return Response(handle_result(result), media_type="image/svg+xml")


@router.post("/claim", response_model=UserSchema)
def claim_account(
    *,
    db: Session = Depends(get_db),
    claim_data: ClaimAccount,
):
    """
    Claim an account using a claim code
    """
    result = AuthenticationService(db).claim_user(obj_in=claim_data)
    if result:
        return handle_result(result)
    return Response(status_code=204)
