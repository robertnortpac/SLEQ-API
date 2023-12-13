from sqlalchemy import String, Column, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.declarative import as_declarative, declared_attr

import uuid
from datetime import datetime
from typing import Optional

@as_declarative()
class Base:
    id = Column(String(36), primary_key=True, default=uuid.uuid4)
    created_on = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String(36), nullable=True)
    updated_on = Column(DateTime, default=None, onupdate=datetime.utcnow)
    updated_by = Column(String(36), nullable=True)

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()