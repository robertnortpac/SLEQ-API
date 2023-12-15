from sqlalchemy.orm import Session

from app.models.sic import Sic
from app.schemas.sic import SicCreate, SicUpdate
from app.crud.base import CRUDBase


class CRUDSic(CRUDBase[Sic, SicCreate, SicUpdate]):
    def __init__(self, db: Session):
        super().__init__(model=Sic, db=db)
    
    def is_unique(self, obj_in: SicCreate, exclude_id: str = None) -> bool:
        query = self.db.query(Sic).filter(Sic.code == obj_in.code)
        if exclude_id:
            query = query.filter(Sic.id != exclude_id)
        sic = query.first()
        if sic:
            return False
        return True