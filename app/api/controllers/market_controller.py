from fastapi import APIRouter, HTTPException, status
from app.resources.market.market_schema import MarketResponse
from typing import List
from resources.market.market_service import get_market_prices_data

router = APIRouter(
    prefix="/market-prices",
    tags=["Market"]
)

@router.get("/", response_model=List[MarketResponse])
async def get_market_prices():
    return await get_market_prices_data()
