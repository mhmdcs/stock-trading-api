import uuid
from sqlalchemy import Column, String, ForeignKey, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base_model import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    symbol = Column(String, nullable=False)
    alert_message = Column(String, nullable=False) # e.g. "Apple Above $300"
    status = Column(String, nullable=False) # e.g. now, recent, old
    priority = Column(String, nullable=False) # e.g. high, medium, low
    alert_rule_id = Column(UUID(as_uuid=True), ForeignKey("alert_rules.id"), nullable=False)
    alert_rule = relationship("AlertRule", back_populates="alerts")
