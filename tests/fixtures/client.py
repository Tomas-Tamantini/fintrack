import pytest
from fastapi.testclient import TestClient

from fintrack.app import app


@pytest.fixture
def client():
    return TestClient(app)
