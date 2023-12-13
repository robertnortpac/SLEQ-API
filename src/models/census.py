from sqlalchemy import Boolean, Column, String, ForeignKey, Date, SmallInteger
from sqlalchemy.orm import relationship

from db.base_class import Base

class Census(Base):
    __tablename__ = "census"

    rfp_id = Column(String(36), ForeignKey("rfp.id"))
    rfp = relationship("Rfp", back_populates="census")

    name = Column(String(150))
    tier_count = Column(SmallInteger)
    is_member_census = Column(Boolean, default=True)
    
    # Members
    members = relationship("Member")

    def __repr__(self):
        return f"<Census {self.name}>"