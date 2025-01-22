from fastapi import HTTPException, status
from app.utils.config import settings
from app.resources.market.market_schema import MarketRequest
import httpx

async def process_market_prices_data(marketRequest: MarketRequest):
    url = "https://twelve-data1.p.rapidapi.com/price"
    headers = {
        "x-rapidapi-host": settings.rapidapi_host,
        "x-rapidapi-key": settings.rapidapi_key,
    }

    market_response = []

    if not marketRequest.symbols:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The ticker symbols list can't be empty. Please provide at least one symbol."
        )

    async with httpx.AsyncClient() as client:
        for symbol in marketRequest.symbols:
            params = {
                "symbol": symbol,
                "outputsize": "30",
                "format": "json",
            }
            try:
                response = await client.get(url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()
                market_response.append({"symbol": symbol, "price": float(data["price"])})
            except (httpx.RequestError, httpx.HTTPStatusError, KeyError, ValueError):
                market_response.append({"symbol": symbol, "price": None})

    return market_response
