from pydantic import BaseModel
from uuid import UUID

class RuleCreate(BaseModel):
    name: str
    threshold_price: float
    symbol: str

class RuleResponse(RuleCreate):
    id: UUID

class RuleUpdate(BaseModel):
    name: str
    threshold_price: float
    symbol: str
