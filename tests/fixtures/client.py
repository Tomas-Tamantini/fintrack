import pytest
from fastapi.testclient import TestClient

from fintrack.api.dependencies.authentication import get_password_handler
from fintrack.api.dependencies.repositories import get_user_repository
from fintrack.app import app


@pytest.fixture
def client(mock_user_repository, mock_password_handler):
    with TestClient(app) as client:
        app.dependency_overrides = {
            get_user_repository: lambda: mock_user_repository,
            get_password_handler: lambda: mock_password_handler,
        }
        yield client
        app.dependency_overrides.clear()
