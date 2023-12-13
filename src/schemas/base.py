from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class BaseInDB(BaseModel):
    id: str = None
    created_on: Optional[datetime] = None
    updated_on: Optional[datetime] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None

class Base(BaseInDB):
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
        }

