from unittest.mock import Mock

import pytest

from fintrack.api.authentication.password_handler import PasswordHandler


@pytest.fixture
def mock_password_handler() -> PasswordHandler:
    mock_handler = Mock(spec=PasswordHandler)
    mock_handler.hash.return_value = "hashed_password"
    return mock_handler
