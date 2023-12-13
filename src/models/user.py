
from sqlalchemy import String, Column, Integer, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from db.base_class import Base


user_company = Table(
    "user_company",
    Base.metadata,
    Column("user_id", String(36), ForeignKey("user.id"), primary_key=True),
    Column("company_id", String(36), ForeignKey("company.id"), primary_key=True),
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
    current_company_id = Column(String(36), ForeignKey("company.id"))

    companies = relationship("Company", secondary=user_company, back_populates="users")



    