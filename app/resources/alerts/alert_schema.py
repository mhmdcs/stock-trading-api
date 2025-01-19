from pydantic import BaseModel
from uuid import UUID

class AlertCreate(BaseModel):
    symbol: str
    alert_message: str
    status: str
    priority: str

class AlertResponse(AlertCreate):
    id: UUID
