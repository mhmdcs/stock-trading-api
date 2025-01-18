from utils.config import settings
import httpx

async def get_market_prices_data():
    url = "https://twelve-data1.p.rapidapi.com/price"
    headers = {
        "x-rapidapi-host": settings.rapidapi_host,
        "x-rapidapi-key": settings.rapidapi_key,
    }
    symbols = ["AAPL", "MSFT", "GOOG", "AMZN", "META", "FCBK"]
    market_response = []

    async with httpx.AsyncClient() as client:
        for symbol in symbols:
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
