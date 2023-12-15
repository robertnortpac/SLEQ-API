from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.tpa import Tpa
from app.schemas.tpa import TpaCreate, TpaUpdate
from app.crud.base import CRUDBase


class CRUDTpa(CRUDBase[Tpa, TpaCreate, TpaUpdate]):
    def __init__(self, db: Session):
        super().__init__(model=Tpa, db=db)
    
    def is_unique(self, obj_in: TpaCreate, exclude_id: str = None) -> bool:
        query = self.db.query(Tpa).filter(Tpa.name == obj_in.name)
        if exclude_id:
            query = query.filter(Tpa.id != exclude_id)
        tpa = query.first()
        if tpa:
            return False
        return True


