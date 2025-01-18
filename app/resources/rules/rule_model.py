import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from db.model_base import Base

class Rule(Base):
    __tablename__ = "rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    threshold_price = Column(Float, nullable=False)
    symbol = Column(String, nullable=False)
    alert = relationship("Alert", back_populates="rule", uselist=False)
