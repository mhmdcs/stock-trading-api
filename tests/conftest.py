from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base_model import Base
from app.api.main import app
from app.db.database import get_db
import pytest

""""
connect to cockroachdb:
cockroach sql --insecure --host=localhost:26257

create trading_test_db database inside the SQL shell by running the following command:
CREATE DATABASE trading_test_db;

check if the database was created successfully:
SHOW DATABASES;
"""

DATABASE_CONNECTION_STRING = "cockroachdb://root@localhost:26257/trading_test_db"

engine = create_engine(DATABASE_CONNECTION_STRING)

TestingSessionLocal = sessionmaker(autoflush=False, bind=engine)

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
