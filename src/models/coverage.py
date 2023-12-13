# from sqlalchemy import Boolean, Column, String, ForeignKey, Date
# from sqlalchemy.orm import relationship

# from db.base_class import Base

# class Coverage(Base):
#     __tablename__ = "coverage"

#     rfp_id = Column(String(36), ForeignKey("rfp.id"))
#     rfp = relationship("Rfp", back_populates="coverage")

#     coverage_type = Column(String(75))


