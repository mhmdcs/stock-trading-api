from utils.config import settings
from .market_schema import MarketRequest
import httpx

async def post_market_prices_data(marketRequest: MarketRequest):
    url = "https://twelve-data1.p.rapidapi.com/price"
    headers = {
        "x-rapidapi-host": settings.rapidapi_host,
        "x-rapidapi-key": settings.rapidapi_key,
    }

    market_response = []

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
