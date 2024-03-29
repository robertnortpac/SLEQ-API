from app.schemas.company import CompanyCreate, CompanyUpdate, CompanyInDB
from app.crud.company import CRUDCompany
from app.crud.user import CRUDUser

from app.services.base import BaseService

from app.utils.service_result import ServiceResult
from app.utils.exceptions.company import *
from app.utils.exceptions.user import *


class CompanyService(BaseService):
    def get_company(self, id: str) -> ServiceResult:
        company = CRUDCompany(self.db).get(id)
        if not company:
            return ServiceResult(CompanyNotFound())
        return ServiceResult(company)

    def get_companies(self, skip: int, limit: int) -> ServiceResult:
        companies = CRUDCompany(self.db).get_multi(skip=skip, limit=limit)
        return ServiceResult(companies)

    def create_company(self, obj_in: CompanyCreate) -> ServiceResult:
        # Check if company name already exists
        company = CRUDCompany(self.db).get_by_name(name=obj_in.name)
        if company:
            return ServiceResult(CompanyAlreadyExists())

        company = CRUDCompany(self.db).create(
            obj_in=obj_in
        )
        return ServiceResult(company)

    def update_company(self, id: str, obj_in: CompanyUpdate) -> ServiceResult:
        company = CRUDCompany(self.db).get(id)
        if not company:
            return ServiceResult(CompanyNotFound())

        company = CRUDCompany(self.db).update(
            db_obj=company, obj_in=obj_in
        )
        return ServiceResult(company)

    def delete_company(self, id: str) -> ServiceResult:
        company = CRUDCompany(self.db).get(id)
        if not company:
            return ServiceResult(CompanyNotFound())

        company = CRUDCompany(self.db).remove(id=id)
        return None

    def get_company_users(self, id: str, skip: int, limit: int) -> ServiceResult:
        company = CRUDCompany(self.db).get(id)
        if not company:
            return ServiceResult(CompanyNotFound())

        users = CRUDCompany(self.db).list_users(db_obj=company, skip=skip, limit=limit)
        return ServiceResult(users)
    
    def add_company_user(self, id: str, user_id: str) -> ServiceResult:
        company = CRUDCompany(self.db).get(id)
        if not company:
            return ServiceResult(CompanyNotFound())
        
        user = CRUDUser(self.db).get(user_id)
        if not user:
            return ServiceResult(UserNotFound())
        
        # Check if user already exists in company
        if user in company.users:
            return ServiceResult(UserAlreadyExistsInCompany())

        user = CRUDCompany(self.db).add_user(db_obj=company, user=user)
        return None
