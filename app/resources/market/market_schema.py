from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional

class MarketRequest(BaseModel):
    """Feed default ticker symbols for testing"""
    symbols: List[str] = Field(
        default=["AAPL", "MSFT", "GOOG", "AMZN", "META", "TSLA", "MHMD"]
    )

class MarketResponse(BaseModel):
    symbol: str
    price: Optional[float]
