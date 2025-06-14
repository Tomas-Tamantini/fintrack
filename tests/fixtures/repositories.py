from unittest.mock import Mock

import pytest

from fintrack.domain.models.user import User
from fintrack.domain.repositories.user_repository import UserRepository


@pytest.fixture
def mock_user_repository(user_stub: User) -> UserRepository:
    mock_repo = Mock(spec=UserRepository)
    mock_repo.create.return_value = user_stub
    return mock_repo
