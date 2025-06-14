import pytest


def create_user_request(
    username: str = "testuser",
    email: str = "test@user.com",
    password: str = "securepassword",
) -> dict[str, str]:
    return {
        "username": username,
        "email": email,
        "password": password,
    }


@pytest.fixture
def valid_create_user_request():
    return create_user_request()


@pytest.fixture
def invalid_email_create_user_request():
    return create_user_request(email="invalid-email")


@pytest.fixture
def short_username_create_user_request():
    return create_user_request(username="ab")


@pytest.fixture
def long_username_create_user_request():
    return create_user_request(username="a" * 51)
