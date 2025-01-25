import pytest
from unittest.mock import patch, AsyncMock, ANY
from fastapi import status
from uuid import uuid4

from app.resources.alert_rules.alert_rule_schema import AlertRuleCreate, AlertRuleUpdate

@pytest.mark.asyncio
@patch("app.resources.alert_rules.alert_rule_service.process_create_alert_rule", new_callable=AsyncMock)
async def test_create_alert_rule(
    mock_create_alert_rule,
    test_client,
    override_get_db
):
    test_payload = {
        "name": "Test Alert",
        "threshold_price": 99.9,
        "symbol": "TEST"
    }
    mock_return_value = {
        "id": str(uuid4()),
        "name": test_payload["name"],
        "threshold_price": test_payload["threshold_price"],
        "symbol": test_payload["symbol"],
    }
    mock_create_alert_rule.return_value = mock_return_value

    response = test_client.post("/alert-rules/", json=test_payload)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_return_value
    mock_create_alert_rule.assert_awaited_once()
    called_args, called_kwargs = mock_create_alert_rule.call_args
    # typically, we'd do something like (db=<AsyncMock>, data=<AlertRuleCreate>)
    # but we can do partial checks:
    assert isinstance(called_kwargs["data"], AlertRuleCreate)
    assert called_kwargs["data"].name == test_payload["name"]


@pytest.mark.asyncio
@patch("app.resources.alert_rules.alert_rule_service.process_get_all_alert_rules", new_callable=AsyncMock)
async def test_get_alert_rules(
    mock_get_all_alert_rules,
    test_client,
    override_get_db
):
    mock_return_value = [
        {
            "id": str(uuid4()),
            "name": "Alert 1",
            "threshold_price": 50.0,
            "symbol": "SYM1",
        },
        {
            "id": str(uuid4()),
            "name": "Alert 2",
            "threshold_price": 150.0,
            "symbol": "SYM2",
        },
    ]
    mock_get_all_alert_rules.return_value = mock_return_value

    response = test_client.get("/alert-rules/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_return_value
    mock_get_all_alert_rules.assert_awaited_once()


@pytest.mark.asyncio
@patch("app.resources.alert_rules.alert_rule_service.process_update_alert_rule", new_callable=AsyncMock)
async def test_update_alert_rule(
    mock_update_alert_rule,
    test_client,
    override_get_db
):
    alert_rule_id = str(uuid4())
    test_payload = {
        "name": "Updated Alert Rule",
        "threshold_price": 200.0,
        "symbol": "UPD"
    }
    mock_return_value = {
        "id": alert_rule_id,
        "name": test_payload["name"],
        "threshold_price": test_payload["threshold_price"],
        "symbol": test_payload["symbol"],
    }
    mock_update_alert_rule.return_value = mock_return_value

    response = test_client.patch(f"/alert-rules/{alert_rule_id}", json=test_payload)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_return_value
    mock_update_alert_rule.assert_awaited_once()
    
    called_args, called_kwargs = mock_update_alert_rule.call_args
    assert str(called_kwargs["id"]) == alert_rule_id
    assert isinstance(called_kwargs["data"], AlertRuleUpdate)


@pytest.mark.asyncio
@patch("app.resources.alert_rules.alert_rule_service.process_delete_alert_rule", new_callable=AsyncMock)
async def test_delete_alert_rule(
    mock_delete_alert_rule,
    test_client,
    override_get_db
):
    alert_rule_id = str(uuid4())
    # the endpoint returns 204 in case a delete is successful
    mock_delete_alert_rule.return_value = True

    response = test_client.delete(f"/alert-rules/{alert_rule_id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    mock_delete_alert_rule.assert_awaited_once()
    called_args, called_kwargs = mock_delete_alert_rule.call_args
    assert str(called_kwargs["id"]) == alert_rule_id
