from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Permission(Base):
    __tablename__ = "permission"

    name = Column(String(75), index=True, unique=True)
    description = Column(String(150), index=True)
    role_id = Column(String(36), ForeignKey("role.id"))
    role = relationship("Role", back_populates="permissions")

    def __repr__(self):
        return f"<Permission {self.name}>"