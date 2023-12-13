from schemas.user import UserCreate, User, UserInDBBase
from crud.user import CRUDUser
from crud.company import CRUDCompany

from services.base import BaseService

from utils.service_result import ServiceResult
from utils.exceptions.user import *
from utils.exceptions.company import *


class UserService(BaseService):
    def get_user(self, id: str) -> ServiceResult:
        user = CRUDUser(self.db).get(id)
        if not user:
            return ServiceResult(UserNotFound())
        return ServiceResult(user)
    
    def get_users(self, skip: int, limit: int) -> ServiceResult:
        users = CRUDUser(self.db).get_multi(skip=skip, limit=limit)
        return ServiceResult(users)
    
    def create_user(self, obj_in: UserCreate) -> ServiceResult:
        # Check if username already exists
        user = CRUDUser(self.db).get_by_username(username=obj_in.username)
        if user:
            return ServiceResult(UserAlreadyExists())
        # Check company_id
        company = CRUDCompany(self.db).get(obj_in.company_id)
        if not company:
            return ServiceResult(CompanyNotFound())
        
        user = CRUDUser(self.db).create(obj_in=obj_in, current_user=self.current_user)
        return ServiceResult(user)
    
    def update_user(self, id: str, obj_in: User) -> ServiceResult:
        user = CRUDUser(self.db).get(id)
        if not user:
            return ServiceResult(UserNotFound())
        # Check company_id
        company = CRUDCompany(self.db).get(obj_in.company_id)
        if not company:
            return ServiceResult(CompanyNotFound())
        
        user = CRUDUser(self.db).update(db_obj=user, obj_in=obj_in, current_user=self.current_user)
        return ServiceResult(user)