from sqlalchemy import Column, String, Integer, Date, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import BaseModel

class Site(BaseModel):
    __tablename__ = "sites"
    name = Column(String(255), nullable=False)
    institution = Column(String(255), nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True, index=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), default="India")
    pin_code = Column(String(10), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    status = Column(String(20), default="ACTIVE")  # ACTIVE, INACTIVE, CLOSED
    activation_date = Column(Date, nullable=True)
    target_enrollment = Column(Integer, nullable=True)
    
    investigators = relationship("Investigator", back_populates="site", lazy="selectin")
    assignments = relationship("SiteAssignment", back_populates="site", lazy="selectin")

class Investigator(BaseModel):
    __tablename__ = "investigators"
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    site_id = Column(String(36), ForeignKey("sites.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    qualification = Column(String(255), nullable=True)
    specialization = Column(String(255), nullable=True)
    experience_years = Column(Integer, nullable=True)
    gcp_trained = Column(Boolean, default=False)
    gcp_certificate_date = Column(Date, nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    
    site = relationship("Site", back_populates="investigators")
    user = relationship("User", foreign_keys=[user_id])

class SiteAssignment(BaseModel):
    __tablename__ = "site_assignments"
    trial_id = Column(String(36), ForeignKey("trials.id"), nullable=False, index=True)
    site_id = Column(String(36), ForeignKey("sites.id"), nullable=False, index=True)
    pi_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    status = Column(String(20), default="PENDING")  # PENDING, ACTIVE, CLOSED
    activation_date = Column(Date, nullable=True)
    deactivation_date = Column(Date, nullable=True)
    target_enrollment = Column(Integer, nullable=True)
    
    trial = relationship("Trial", back_populates="sites")
    site = relationship("Site", back_populates="assignments")
    pi = relationship("User", foreign_keys=[pi_id])
