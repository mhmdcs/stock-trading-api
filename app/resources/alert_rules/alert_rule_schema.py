from pydantic import BaseModel
from uuid import UUID

class AlertRuleCreate(BaseModel):
    name: str
    threshold_price: float
    symbol: str

class AlertRuleResponse(AlertRuleCreate):
    id: UUID

class AlertRuleUpdate(BaseModel):
    name: str
    threshold_price: float
    symbol: str
