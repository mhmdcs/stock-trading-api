import pytest
from unittest.mock import patch, AsyncMock
from fastapi import status
from uuid import uuid4

@pytest.mark.asyncio
@patch("app.resources.alerts.alert_service.process_get_all_alerts", new_callable=AsyncMock)
async def test_get_alerts(
    mock_get_all_alerts,
    test_client,
    override_get_db
):
    mock_return_value = [
        {
            "id": str(uuid4()),
            "symbol": "AAPL",
            "alert_message": "Price crossed threshold",
            "status": "active",
            "priority": "high"
        },
        {
            "id": str(uuid4()),
            "symbol": "TSLA",
            "alert_message": "Volume spike detected",
            "status": "inactive",
            "priority": "medium"
        },
    ]
    mock_get_all_alerts.return_value = mock_return_value

    response = test_client.get("/alerts/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_return_value


    mock_get_all_alerts.assert_awaited_once()
