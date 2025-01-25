import pytest
from unittest.mock import patch, AsyncMock
from fastapi import status
from app.resources.market.market_schema import MarketRequest

@pytest.mark.asyncio
@patch("app.resources.market.market_service.process_market_prices_data", new_callable=AsyncMock)
async def test_post_market_prices_success(mock_process_data, test_client):
    test_payload = {
        "symbols": ["AAPL", "TSLA"]
    }
    mock_return_value = [
        {"symbol": "AAPL", "price": 150.25},
        {"symbol": "TSLA", "price": 700.10}
    ]
    mock_process_data.return_value = mock_return_value

    response = test_client.post("/market-prices/", json=test_payload)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_return_value
    
    test_payload_parsed = MarketRequest(**test_payload)
    mock_process_data.assert_awaited_once_with(test_payload_parsed)

@pytest.mark.asyncio
@patch("app.resources.market.market_service.process_market_prices_data", new_callable=AsyncMock)
async def test_post_market_prices_empty_symbols(mock_process_data, test_client):
    test_payload = {
        "symbols": []
    }
    
    # simulate the service raising an HTTPException
    from fastapi import HTTPException, status
    mock_process_data.side_effect = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="The ticker symbols list can't be empty. Please provide at least one symbol."
    )

    response = test_client.post("/market-prices/", json=test_payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "The ticker symbols list can't be empty. Please provide at least one symbol."
    }
    
    test_payload_parsed = MarketRequest(**test_payload)
    mock_process_data.assert_awaited_once_with(test_payload_parsed)