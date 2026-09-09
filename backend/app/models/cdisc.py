from sqlalchemy import Column, String, Boolean, Text
from .base import BaseModel

class CDISCMapping(BaseModel):
    __tablename__ = "cdisc_mappings"
    internal_entity = Column(String(100), nullable=False)
    internal_field = Column(String(100), nullable=False)
    cdisc_domain = Column(String(10), nullable=False)
    cdisc_variable = Column(String(30), nullable=False)
    transformation_rule = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
