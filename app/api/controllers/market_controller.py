from fastapi import APIRouter, Body
from app.resources.market.market_schema import MarketResponse, MarketRequest
from typing import List
from app.resources.market.market_service import process_market_prices_data

router = APIRouter(
    prefix="/market-prices",
    tags=["Market"]
)

@router.post("/", response_model=List[MarketResponse])
async def post_market_prices(request: MarketRequest = Body(...)):
    return await process_market_prices_data(request)
