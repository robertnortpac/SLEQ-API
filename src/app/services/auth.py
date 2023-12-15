import pyotp

import qrcode
from qrcode.image.svg import SvgImage
from lxml import etree

from app.schemas.auth import ClaimAccount, Login
from app.schemas.user import UserInDB
from app.crud.user import CRUDUser

from app.services.base import BaseService

from app.utils.service_result import ServiceResult
from app.utils.exceptions.auth import *
from app.utils.exceptions.user import *
from app.core.auth.security import verify_password, get_password_hash, validate_otp
from app.core.auth.jwt import create_access_token


class AuthenticationService(BaseService):
    def authenticate_user(self, obj_in: Login) -> ServiceResult:
        user = CRUDUser(self.db).get_by_username(username=obj_in.username)
        if not user:
            return ServiceResult(AuthenticationError())
        if not user.is_active:
            return ServiceResult(AuthenticationError())
        if not verify_password(obj_in.password, user.secret):
            return ServiceResult(InvalidPassword())
        if user.otp_enabled:
            if not validate_otp(otp=obj_in.otp, secret=user.otp_secret):
                return ServiceResult(InvalidOTP())
        token = create_access_token(user=user)
        return ServiceResult(token)
    
    def claim_user(self, obj_in: ClaimAccount) -> ServiceResult:
        user = CRUDUser(self.db).get_by_claim_code(claim_code=obj_in.claim_code)
        if not user:
            return ServiceResult(InvalidClaimCode())
        if user.is_claimed:
            return ServiceResult(AccountAlreadyClaimed())
        if obj_in.password != obj_in.password_confirm:
            return ServiceResult(PasswordsDontMatch())
        if not validate_otp(otp=obj_in.otp, secret=user.otp_secret):
            return ServiceResult(InvalidOTP())
        
        obj_data = obj_in.model_dump()
        hashed_password = get_password_hash(obj_data["password"])
        del obj_data["password"]
        del obj_data["password_confirm"]
        obj_data["secret"] = hashed_password
        obj_data["is_claimed"] = True
        obj_data["claim_code"] = None
        use_obj_in = UserInDB.model_validate(obj_data)
        user = CRUDUser(self.db).update(db_obj=user, obj_in=use_obj_in)
        return ServiceResult(user)
    
    def generate_qr_by_claim_code(self, claim_code: str) -> ServiceResult:
        user = CRUDUser(self.db).get_by_claim_code(claim_code=claim_code)
        if not user:
            return ServiceResult(UserNotFound())
        if user.is_claimed:
            return ServiceResult(AccountAlreadyClaimed())
        totp = pyotp.TOTP(user.otp_secret)
        qr_url = totp.provisioning_uri(user.username, issuer_name="SLEQ API")
        img = qrcode.make(qr_url, image_factory=SvgImage)
        svg = etree.tostring(img.get_image())
        return ServiceResult(svg)
    
