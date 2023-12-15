from sqlalchemy import Boolean, Column, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Tpa(Base):
    __tablename__ = "tpa"

    name = Column(String(150), unique=True, index=True)
    is_active = Column(Boolean(), default=True)
    tpac_id = Column(String(36), unique=True, index=True)

    