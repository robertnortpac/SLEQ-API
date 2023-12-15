from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate, CompanyInDB

from app.crud.base import CRUDBase


class CRUDCompany(CRUDBase[Company, CompanyCreate, CompanyUpdate]):
    def __init__(self, db: Session):
        super().__init__(model=Company, db=db)

    def get_by_name(self, *, name: str) -> Optional[Company]:
        return self.db.query(Company).filter(Company.name == name).first()
    
    def list_users(self, *, db_obj: Company, skip: int = 0, limit: int = 100) -> list[User]:
        return db_obj.users[skip:skip+limit]
    
    def add_user(self, *, db_obj: Company, user: User) -> bool:
        db_obj.users.append(user)
        self.db.add(db_obj)
        self.db.commit()
        return True
    