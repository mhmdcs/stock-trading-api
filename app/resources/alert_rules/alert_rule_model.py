import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Float
from sqlalchemy.orm import relationship
from app.db.base_model import Base

class AlertRule(Base):
    __tablename__ = "alert_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False, unique=True) # e.g. "Apple Below $150", "Tesla Below $150"
    threshold_price = Column(Float, nullable=False)
    symbol = Column(String, nullable=False)
    alerts = relationship("Alert", back_populates="alert_rule", cascade="all, delete")
