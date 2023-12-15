from typing import Optional

from pydantic import BaseModel

from app.schemas.base import BaseInDB

class SicBase(BaseModel):
    code: Optional[str] = None
    description: Optional[str] = None

class SicCreate(SicBase):
    code: str
    description: str
    tpac_id: Optional[str] = None

class SicUpdate(SicBase):
    description: str = None

class SicInDBBase(BaseInDB, SicBase):
    pass

class Sic(SicInDBBase):
    pass

class SicInDB(SicInDBBase):
    tpac_id: Optional[str] = None