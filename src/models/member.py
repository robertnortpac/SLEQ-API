from sqlalchemy import Boolean, Column, String, ForeignKey, Date, SmallInteger
from sqlalchemy.orm import relationship

from db.base_class import Base

class Member(Base):
    __tablename__ = "member"

    census_id = Column(String(36), ForeignKey("census.id"))
    census = relationship("Census", back_populates="members")

    # Member Information
    first_name = Column(String(100))
    last_name = Column(String(100))
    gender = Column(String(1))
    date_of_birth = Column(Date)
    zip_code = Column(String(5))
    plan_elected = Column(String(100))
    relationship_to_insured = Column(String(2))
    tier_coverage = Column(String(3))
    is_cobra = Column(Boolean, default=False)
    is_retiree = Column(Boolean, default=False)

    # Member Status
    declined_coverage = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Member {self.first_name} {self.last_name}>"
