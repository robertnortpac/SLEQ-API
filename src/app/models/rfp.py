from sqlalchemy import Boolean, Column, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Rfp(Base):
    __tablename__ = "rfp"

    friendly_label = Column(String(150))

    # Group Information
    group_name = Column(String(75))
    address_street_1 = Column(String(100))
    address_street_2 = Column(String(100))
    address_city = Column(String(150))
    address_state = Column(String(2))
    address_zip = Column(String(5))
    has_claims_experience = Column(Boolean, default=False)
    has_current_coverage = Column(Boolean, default=False)

    sic_id = Column(String(36), ForeignKey("sic.id"))
    sic_code = relationship("Sic")

    tpa_id = Column(String(36), ForeignKey("tpa.id"))
    tpa = relationship("Tpa")

    # Underwriting Information
    effective_date = Column(Date)
    request_by_date = Column(Date)
    # assigned_underwriter_id = Column(String(36), ForeignKey("underwriter.id"))
    # assigned_underwriter = relationship("Underwriter", back_populates="rfps")
    
    # RFP Status
    is_active = Column(Boolean, default=True)
    is_assigned = Column(Boolean, default=False)
    is_declined = Column(Boolean, default=False)
    is_expired = Column(Boolean, default=False)
    is_on_hold = Column(Boolean, default=False)
    is_submitted = Column(Boolean, default=False)
    is_withdrawn = Column(Boolean, default=False)
    is_rejected = Column(Boolean, default=False)
    is_quoted = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)

    # RFP Census
    census = relationship("Census", cascade="all, delete-orphan")

    company_id = Column(String(36), ForeignKey("company.id"))











    

