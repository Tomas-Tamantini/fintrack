import pytest

from fintrack.domain.models.user import User


@pytest.fixture
def user_stub():
    return User(
        id=123,
        username="testuser",
        email="test@user.com",
        hashed_password="hashedpassword",
    )
