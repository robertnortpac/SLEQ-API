from typing import Optional
from pydantic import BaseModel

from .base import BaseInDB

class CompanyBase(BaseModel):
    name: str
    is_active: Optional[bool] = True

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(CompanyBase):
    pass

class CompanyInDBBase(BaseInDB, CompanyBase):
    pass

class Company(CompanyInDBBase):
    pass

class CompanyInDB(CompanyInDBBase):
    pass