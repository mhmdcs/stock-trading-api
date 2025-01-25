import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.api.main import app

@pytest.fixture(scope="session")
def test_client():
    with TestClient(app) as client:
        yield client

@pytest.fixture
def mock_db_session():
    return AsyncMock()

@pytest.fixture
def override_get_db(mock_db_session):
    with patch("app.db.database.get_db", return_value=mock_db_session):
        yield mock_db_session
