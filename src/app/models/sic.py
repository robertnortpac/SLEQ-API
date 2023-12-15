from sqlalchemy import Boolean, Column, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Sic(Base):
    __tablename__ = "sic"

    code = Column(String(4), unique=True, index=True)
    description = Column(String(150))

    tpac_id = Column(String(36), unique=True, index=True)