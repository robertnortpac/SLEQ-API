from app.schemas.tpa import TpaCreate, TpaUpdate, TpaInDB
from app.crud.tpa import CRUDTpa

from app.services.base import BaseService

from app.utils.service_result import ServiceResult
from app.utils.exceptions.tpa import *


class TpaSevice(BaseService):
    def get_tpa(self, id: str) -> ServiceResult:
        tpa = CRUDTpa(self.db).get(id)
        if not tpa:
            return ServiceResult(TpaNotFound())
        return ServiceResult(tpa)

    def get_tpas(self, skip, limit) -> ServiceResult:
        tpas = CRUDTpa(self.db).get_multi(skip=skip, limit=limit)
        return ServiceResult(tpas)

    def create_tpa(self, obj_in: TpaCreate) -> ServiceResult:
        if not CRUDTpa(self.db).is_unique(obj_in=obj_in):
            return ServiceResult(TpaAlreadyExists())

        obj_data = obj_in.model_dump(exclude_unset=True)

        if self.current_user:
            obj_data["created_by"] = self.current_user.id

        use_obj_in = TpaInDB.model_validate(obj_data)

        tpa = CRUDTpa(self.db).create(obj_in=use_obj_in)
        return ServiceResult(tpa)

    def update_tpa(self, id: str, obj_in: TpaUpdate) -> ServiceResult:
        tpa = CRUDTpa(self.db).get(id)
        if not tpa:
            return ServiceResult(TpaNotFound())

        if not CRUDTpa(self.db).is_unique(obj_in=obj_in, exclude_id=id):
            return ServiceResult(TpaAlreadyExists())

        obj_data = obj_in.model_dump(exclude_unset=True)

        if self.current_user:
            obj_data["updated_by"] = self.current_user.id

        use_obj_in = TpaInDB.model_validate(obj_data)

        tpa = CRUDTpa(self.db).update(db_obj=tpa, obj_in=use_obj_in)
        return ServiceResult(tpa)

    def delete_tpa(self, id: str) -> ServiceResult:
        tpa = CRUDTpa(self.db).get(id)
        if not tpa:
            return ServiceResult(TpaNotFound())

        tpa = CRUDTpa(self.db).delete(id=id)
        return None
