from unittest.mock import Mock

import pytest

from fintrack.api.authentication.jwt_service import JWTService
from fintrack.api.authentication.password_handler import PasswordHandler


@pytest.fixture
def mock_password_handler() -> PasswordHandler:
    mock_handler = Mock(spec=PasswordHandler)
    mock_handler.hash.return_value = "hashed_password"
    return mock_handler


@pytest.fixture
def mock_jwt_service() -> JWTService:
    mock_service = Mock(spec=JWTService)
    return mock_service
