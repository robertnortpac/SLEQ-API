from typing import Optional
from pydantic import BaseModel

from .base import BaseInDB

class PermissionBase(BaseModel):
    name: str
    description: Optional[str] = None

class PermissionCreate(PermissionBase):
    name: str
    description: Optional[str] = None

class PermissionUpdate(PermissionBase):
    name: Optional[str] = None
    description: Optional[str] = None

class PermissionInDBBase(BaseInDB, PermissionBase):
    pass

class Permission(PermissionInDBBase):
    pass

class PermissionInDB(PermissionInDBBase):
    pass