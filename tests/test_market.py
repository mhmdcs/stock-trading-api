from app.resources.market.market_schema import MarketRequest

def mock_market_service(market_request: MarketRequest):
    return [{"symbol": "AAPL", "price": 145.0}, {"symbol": "TSLA", "price": 750.0}]

def test_post_market_prices(client, monkeypatch):
    monkeypatch.setattr("app.resources.market.market_service.process_market_prices_data", mock_market_service)
    
    data = {"symbols": ["AAPL", "TSLA"]}
    res = client.post("/market-prices/", json=data)
    assert res.status_code == 200
    assert len(res.json()) == 2
    assert res.json()[0]["symbol"] == "AAPL"
    assert res.json()[1]["price"] >= 0.0
