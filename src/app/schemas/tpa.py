from typing import Optional
from pydantic import BaseModel

from .base import BaseInDB

class TpaBase(BaseModel):
    name: str

class TpaCreate(TpaBase):
    name: str = "TPA Name"

class TpaUpdate(TpaBase):
    is_active: Optional[bool] = True

class TpaInDBBase(BaseInDB, TpaBase):
    pass

class Tpa(TpaInDBBase):
    pass

class TpaInDB(TpaInDBBase):
    tpac_id: Optional[str] = None