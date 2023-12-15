from app.schemas.sic import SicCreate, SicUpdate, SicInDB
from app.crud.sic import CRUDSic

from app.services.base import BaseService

from app.utils.service_result import ServiceResult
from app.utils.exceptions.sic import *

class SicService(BaseService):
    def get_sic(self, id: str) -> ServiceResult:
        sic = CRUDSic(self.db).get(id)
        if not sic:
            return ServiceResult(SicNotFound())
        return ServiceResult(sic)
    
    def get_sics(self, skip, limit) -> ServiceResult:
        sics = CRUDSic(self.db).get_multi(skip=skip, limit=limit)
        return ServiceResult(sics)
    
    def create_sic(self, obj_in: SicCreate) -> ServiceResult:
        if not CRUDSic(self.db).is_unique(obj_in=obj_in):
            return ServiceResult(SicAlreadyExists())

        obj_data = obj_in.model_dump(exclude_unset=True)

        if self.current_user:
            obj_data["created_by"] = self.current_user.id

        use_obj_in = SicInDB.model_validate(obj_data)

        sic = CRUDSic(self.db).create(obj_in=use_obj_in)
        return ServiceResult(sic)
    
    def update_sic(self, id: str, obj_in: SicUpdate) -> ServiceResult:
        sic = CRUDSic(self.db).get(id)
        if not sic:
            return ServiceResult(SicNotFound())

        if not CRUDSic(self.db).is_unique(obj_in=obj_in, exclude_id=id):
            return ServiceResult(SicAlreadyExists())

        obj_data = obj_in.model_dump(exclude_unset=True)

        if self.current_user:
            obj_data["updated_by"] = self.current_user.id

        use_obj_in = SicInDB.model_validate(obj_data)

        sic = CRUDSic(self.db).update(db_obj=sic, obj_in=use_obj_in)
        return ServiceResult(sic)
    
    def delete_sic(self, id: str) -> ServiceResult:
        sic = CRUDSic(self.db).get(id)
        if not sic:
            return ServiceResult(SicNotFound())

        sic = CRUDSic(self.db).delete(id=id)
        return None

