from pydantic import BaseModel

class AlertCreate(BaseModel):
    symbol: str

class AlertResponse(AlertCreate):
    rule_id: int
