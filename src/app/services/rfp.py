from app.schemas.rfp import RfpCreate, RfpUpdate
from app.crud.rfp import CRUDRfp

from app.services.base import BaseService

from app.utils.service_result import ServiceResult
from app.utils.exceptions.rfp import *


class RFPService(BaseService):
    def get_rfp(self, id: str) -> ServiceResult:
        rfp = CRUDRfp(self.db).get(id)
        if not rfp:
            return ServiceResult(RfpNotFound())
        return ServiceResult(rfp)
    
    def get_rfps(self, skip, limit) -> ServiceResult:
        rfps = CRUDRfp(self.db).get_multi(skip=skip, limit=limit)
        return ServiceResult(rfps)
    
    def create_rfp(self, obj_in: RfpCreate) -> ServiceResult:
        if not CRUDRfp(self.db).is_unique(obj_in=obj_in):
            return ServiceResult(RfpAlreadyExists())
        
        # Validate tpa_id

        tpa = CRUDTpa(self.db).get(obj_in.tpa_id)
        if not tpa:
            return ServiceResult(TpaNotFound())

        rfp = CRUDRfp(self.db).create(obj_in=obj_in, current_user=self.current_user)
        return ServiceResult(rfp)
