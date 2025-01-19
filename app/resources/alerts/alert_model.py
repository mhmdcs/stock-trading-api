import uuid
from sqlalchemy import Column, String, ForeignKey, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.model_base import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    symbol = Column(String, nullable=False)
    alert_rule_id = Column(UUID(as_uuid=True), ForeignKey("alert_rules.id"), nullable=False)
    alert_message = Column(Text, nullable=False) # e.g. "Apple Above $300"
    status = Column(String, default="new") # e.g. "new", "read", "acknowledged"
    priority = Column(String, nullable=True) # e.g. "low", "medium", "high"
    alert_rule = relationship("AlertRule", back_populates="alerts")
