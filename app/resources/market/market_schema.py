from pydantic import BaseModel
from typing import Optional

class MarketResponse(BaseModel):
    symbol: str
    price: Optional[float]
