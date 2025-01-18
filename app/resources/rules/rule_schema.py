from pydantic import BaseModel

class RuleCreate(BaseModel):
    name: str
    threshold_price: float
    symbol: str

class RuleResponse(RuleCreate):
    id: int

class RuleUpdate(BaseModel):
    name: str
    threshold_price: float
    symbol: str
