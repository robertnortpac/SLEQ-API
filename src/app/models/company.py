from sqlalchemy import String, Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Company(Base):
    __tablename__ = "company"

    name = Column(String(150))
    is_active = Column(Boolean, default=True)

    users = relationship("User", cascade="all, delete-orphan")