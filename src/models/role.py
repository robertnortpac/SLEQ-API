from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from db.base_class import Base

class Role(Base):
    __tablename__ = "role"

    name = Column(String(75), index=True, unique=True)
    description = Column(String(150), index=True)
    permissions = relationship("Permission", back_populates="role", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Role {self.name}>"