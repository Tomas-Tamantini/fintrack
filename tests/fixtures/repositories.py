from unittest.mock import Mock

import pytest

from fintrack.domain.models.user import User
from fintrack.domain.repositories.user_repository import UserRepository


@pytest.fixture
def mock_user_repository():
    mock_repo = Mock(spec=UserRepository)
    mock_repo.create.return_value = User(
        id=1,
        username="testuser",
        email="test@user.com",
        hashed_password="hashedpassword",
    )
    return mock_repo
