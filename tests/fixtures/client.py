import pytest
from fastapi.testclient import TestClient

from fintrack.api.dependencies.repositories import get_user_repository
from fintrack.app import app


@pytest.fixture
def client(mock_user_repository):
    with TestClient(app) as client:
        app.dependency_overrides = {
            get_user_repository: lambda: mock_user_repository
        }
        yield client
        app.dependency_overrides.clear()
