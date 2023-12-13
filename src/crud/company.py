from typing import Optional

from sqlalchemy.orm import Session

from models.user import User
from models.company import Company
from schemas.company import CompanyCreate, CompanyUpdate, CompanyInDB

from crud.base import CRUDBase


class CRUDCompany(CRUDBase[Company, CompanyCreate, CompanyUpdate]):
    def __init__(self, db: Session):
        super().__init__(model=Company, db=db)

    def get_by_name(self, *, name: str) -> Optional[Company]:
        return self.db.query(Company).filter(Company.name == name).first()
    
    def create(self, *, obj_in: CompanyCreate, current_user: User = None) -> Company:
        db_obj = Company(
            name=obj_in.name,
            is_active=obj_in.is_active,
        )
        if current_user:
            setattr(db_obj, "created_by", current_user.id)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def update(self, *, db_obj: Company, obj_in: CompanyUpdate, current_user: User = None) -> Company:
        update_data = obj_in.model_dump(exclude_unset=True)
        use_obj_in = CompanyInDB.model_validate(update_data)
        return super().update(db_obj=db_obj, obj_in=use_obj_in, current_user=current_user)
    
    def list_users(self, *, db_obj: Company, skip: int = 0, limit: int = 100) -> list[User]:
        return db_obj.users[skip:skip+limit]
    