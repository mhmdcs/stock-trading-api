import uuid
from sqlalchemy import Column, String, ForeignKey, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.model_base import Base

class Alert(Base):
    __tablename__ = "alerts"
    __table_args__ = {"extend_existing": True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    symbol = Column(String, nullable=False)
    alert_rule_id = Column(UUID(as_uuid=True), ForeignKey("alert_rules.id"), nullable=False)
    alert_message = Column(String, nullable=False) # e.g. "Apple Above $300"
    alert_rule = relationship("AlertRule", back_populates="alerts")
