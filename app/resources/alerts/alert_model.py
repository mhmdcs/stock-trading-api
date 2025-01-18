from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.model_base import Base

class Alert(Base):
    __tablename__ = "alerts"

    symbol = Column(String, primary_key=True, nullable=False)
    rule_id = Column(UUID(as_uuid=True), ForeignKey("rules.id"), nullable=False)
    rule = relationship("Rule", back_populates="alert")
