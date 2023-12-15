import pyotp

from app.schemas.user import UserCreate, UserInDB, UserUpdate
from app.schemas.auth import ClaimAccount, Login
from app.crud.user import CRUDUser
from app.crud.company import CRUDCompany

from app.services.base import BaseService

from app.utils.service_result import ServiceResult
from app.utils.exceptions.user import *
from app.utils.exceptions.company import *
from app.utils.generator import generate_claim_code, generate_random_password
from app.core.auth.security import verify_password, get_password_hash


class UserService(BaseService):
    def get_user(self, id: str) -> ServiceResult:
        user = CRUDUser(self.db).get(id)
        if not user:
            return ServiceResult(UserNotFound())
        return ServiceResult(user)

    def get_users(self, skip: int, limit: int) -> ServiceResult:
        users = CRUDUser(self.db).get_multi(skip=skip, limit=limit)
        return ServiceResult(users)

    def get_user_by_username(self, username: str) -> ServiceResult:
        user = CRUDUser(self.db).get_by_username(username=username)
        if not user:
            return ServiceResult(UserNotFound())
        return ServiceResult(user)

    def create_user(self, obj_in: UserCreate) -> ServiceResult:
        # Check if username already exists
        user = CRUDUser(self.db).get_by_username(username=obj_in.username)
        if user:
            return ServiceResult(UserAlreadyExists())
        # Check company_id
        if obj_in.company_id:
            company = CRUDCompany(self.db).get(obj_in.company_id)
            if not company:
                return ServiceResult(CompanyNotFound())

        obj_data = obj_in.model_dump()

        # Conversion
        if obj_data.get("password"):
            hashed_password = get_password_hash(obj_data["password"])
            del obj_data["password"]
        else:
            hashed_password = get_password_hash(generate_random_password())
        obj_data["secret"] = hashed_password

        if obj_data["otp_enabled"]:
            obj_data["otp_secret"] = pyotp.random_base32()
            obj_data["claim_code"] = generate_claim_code()

        # Set created_by
        if self.current_user:
            obj_data["created_by"] = self.current_user.id

        use_obj_in = UserInDB.model_validate(obj_data)

        user = CRUDUser(self.db).create(obj_in=use_obj_in)

        # Add user to company
        if obj_in.company_id:
            result = CRUDCompany(self.db).add_user(db_obj=company, user=user)

        return ServiceResult(user)

    def update_user(self, id: str, obj_in: UserUpdate) -> ServiceResult:
        user = CRUDUser(self.db).get(id)
        if not user:
            return ServiceResult(UserNotFound())

        user = CRUDUser(self.db).get(id)

        # Check if username already exists
        is_unique = CRUDUser(self.db).is_uniquely_named(user_in=user, obj_in=obj_in)
        print(is_unique)
        if not is_unique:
            return ServiceResult(UserAlreadyExists())

        obj_data = obj_in.model_dump()

        # Conversion
        if obj_data.get("password"):
            hashed_password = get_password_hash(obj_data["password"])
            del obj_data["password"]
            obj_data["secret"] = hashed_password

        if self.create_user:
            obj_data["updated_by"] = self.current_user.id

        use_obj_in = UserInDB.model_validate(obj_data)

        user = CRUDUser(self.db).update(db_obj=user, obj_in=use_obj_in)
        return ServiceResult(user)

