from typing import Optional

from sqlalchemy.orm import Session

from app.models.rfp import Rfp
from app.schemas.rfp import RfpCreate, RfpUpdate
from app.crud.base import CRUDBase


class CRUDRfp(CRUDBase[Rfp, RfpCreate, RfpUpdate]):
    def __init__(self, db: Session):
        super().__init__(model=Rfp, db=db)

    def is_unique(self, *, obj_in: RfpCreate) -> bool:
        rfp = (
            self.db.query(Rfp)
            .filter(
                Rfp.group_name == obj_in.group_name,
                Rfp.address_street_1 == obj_in.address_street_1,
                Rfp.address_city == obj_in.address_city,
                Rfp.address_state == obj_in.address_state,
                Rfp.address_zip == obj_in.address_zip,
                Rfp.effective_date == obj_in.effective_date,
            )
            .first()
        )
        if rfp:
            return False
        return True

    def get_by_user(self, *, user_id: str) -> Optional[Rfp]:
        return self.db.query(Rfp).filter(Rfp.created_by == user_id).all()
