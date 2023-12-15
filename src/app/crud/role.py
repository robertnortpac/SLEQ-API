from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.role import Role
from schemas import RoleCreate, RoleUpdate, RoleInDB
from app.crud.base import CRUDBase


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    def get_by_name(self, db_session: Session, *, name: str) -> Optional[Role]:
        return db_session.query(Role).filter(Role.name == name).first()
    
    def get_multi(self, db_session: Session, *, skip=0, limit=100) -> List[Role]:
        return super().get_multi(db_session, skip=skip, limit=limit)

    def create(self, db_session: Session, *, obj_in: RoleCreate) -> Role:
        db_obj = Role(
            name=obj_in.name,
            description=obj_in.description,
        )
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

    def update(self, db_session: Session, *, db_obj: Role, obj_in: RoleUpdate) -> Role:
        return super().update(db_session, db_obj=db_obj, obj_in=obj_in)
    
    def delete(self, db_session: Session, *, db_obj: Role) -> Role:
        return super().remove(db_session, db_obj=db_obj)

# role = CRUDRole(Role)