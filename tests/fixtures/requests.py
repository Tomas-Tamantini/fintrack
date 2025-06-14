import pytest


@pytest.fixture
def valid_create_user_request():
    return {
        "username": "testuser",
        "email": "test@user.com",
        "password": "securepassword",
    }


@pytest.fixture
def invalid_email_create_user_request():
    return {
        "username": "testuser",
        "email": "invalid-email",
        "password": "securepassword",
    }


@pytest.fixture
def short_username_create_user_request():
    return {
        "username": "ab",
        "email": "a@b.com",
        "password": "securepassword",
    }


@pytest.fixture
def long_username_create_user_request():
    return {
        "username": "a" * 51,
        "email": "a@b.com",
        "password": "securepassword",
    }
