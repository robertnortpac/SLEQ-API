from typing import Optional

from sqlalchemy.orm import Session

from models.user import User
from models.rfp import Rfp
from schemas.rfp import RfpCreate, RfpUpdate
from crud.base import CRUDBase


class CRUDRfp(CRUDBase[Rfp, RfpCreate, RfpUpdate]):
    def __init__(self, db: Session):
        super().__init__(model=Rfp, db=db)

    def create(self, *, obj_in: RfpCreate, current_user: User = None) -> Rfp:
        db_obj = Rfp(
            group_name=obj_in.group_name,
            address_street_1=obj_in.address_street_1,
            address_street_2=obj_in.address_street_2,
            address_city=obj_in.address_city,
            address_state=obj_in.address_state,
            address_zip=obj_in.address_zip,
            has_claims_experience=obj_in.has_claims_experience,
            has_current_coverage=obj_in.has_current_coverage,
            effective_date=obj_in.effective_date,
        )
        if current_user:
            setattr(db_obj, "created_by", current_user.id)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(
        self, *, db_obj: Rfp, obj_in: RfpUpdate, current_user: User = None
    ) -> Rfp:
        return super().update(db_obj=db_obj, obj_in=obj_in, current_user=current_user)

    def delete(self, *, id: str) -> Rfp:
        return super().delete(id=id)

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
