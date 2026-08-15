import pytest
from fastapi.testclient import TestClient

from app import app
from database.connection import Base, engine


@pytest.fixture(scope="session", autouse=True)
def setup_database() -> None:
    Base.metadata.create_all(bind=engine)


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)