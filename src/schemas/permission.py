from typing import Optional
from pydantic import BaseModel

class PermissionBase(BaseModel):
    name: str
    description: Optional[str] = None

class PermissionCreate(PermissionBase):
    name: str
    description: Optional[str] = None

class PermissionUpdate(PermissionBase):
    name: Optional[str] = None
    description: Optional[str] = None

class PermissionInDBBase(PermissionBase):
    id: str

    class Config:
        from_attributes = True

class Permission(PermissionInDBBase):
    pass

class PermissionInDB(PermissionInDBBase):
    pass