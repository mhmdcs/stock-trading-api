from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from db.model_base import Base

class Rule(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    threshold_price = Column(Float, nullable=False)
    symbol = Column(String, nullable=False)
    alert = relationship("Alert", back_populates="rule", uselist=False)
