
from sqlalchemy import String, Column, Integer, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.base_class import Base

from enum import Enum

user_role = Table(
    "user_role",
    Base.metadata,
    Column("user_id", String(36), ForeignKey("user.id"), primary_key=True),
    Column("role_id", String(36), ForeignKey("role.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "user"

    username = Column(String(75), unique=True, index=True)
    email = Column(String(150), unique=True, index=True)
    secret = Column(String(150))
    otp_enabled = Column(Boolean, default=False)
    otp_secret = Column(String(150))
    claim_code = Column(String(150))
    is_claimed = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    company_id = Column(String(36), ForeignKey("company.id"))
    company = relationship("Company", back_populates="users")

    roles = relationship("Role", secondary="user_role")

    class Permissions(Enum):
        read = "user:read"
        write = "user:write"
        update = "user:update"
        delete = "user:delete"
        all = "user:all"