from fastapi import APIRouter, HTTPException, status
from utils.config import settings

import httpx
# from resources.market.market_service import get_market_data

router = APIRouter(
    prefix="/market-prices",
    tags=["Market"]
)

@router.get("/")
async def get_market_prices():
    url = "https://twelve-data1.p.rapidapi.com/price"
    headers = {
        "x-rapidapi-host": settings.rapidapi_host,
        "x-rapidapi-key": settings.rapidapi_key,
    }
    params = {
        "symbol": "META",
        "outputsize": "30",
        "format": "json",
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            # return response.json()
            response.raise_for_status()
            data = response.json() # Parse JSON response
            return {"data": data}
        except httpx.RequestError as exc:
            # Handle request exceptions e.g. network issues
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error while making request: {exc}")
        except httpx.HTTPStatusError as exc:
            # Handle resposne-related errors
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"Error resposne {exc.response.status_code} from external API: {exc.response.text}"
            )

# @router.get()
# def get_market_data_route():
#     return get_market_data()
