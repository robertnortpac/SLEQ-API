from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

role_permission = Table(
    "role_permission",
    Base.metadata,
    Column("role_id", String(36), ForeignKey("role.id")),
    Column("permission_id", String(36), ForeignKey("permission.id")),
)

class Role(Base):
    __tablename__ = "role"

    name = Column(String(75), index=True, unique=True)
    description = Column(String(150), index=True)
    permissions = relationship("Permission", secondary="role_permission")

    def __repr__(self):
        return f"<Role {self.name}>"