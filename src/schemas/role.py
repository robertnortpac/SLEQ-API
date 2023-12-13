from typing import Optional
from pydantic import BaseModel

from .base import BaseInDB

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    name: str
    description: Optional[str] = None

class RoleUpdate(RoleBase):
    name: Optional[str] = None
    description: Optional[str] = None

class RoleInDBBase(BaseInDB, RoleBase):
    id: str

    class Config:
        from_attributes = True

class Role(RoleInDBBase):
    pass

class RoleInDB(RoleInDBBase):
    pass