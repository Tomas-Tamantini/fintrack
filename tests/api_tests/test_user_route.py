from http import HTTPStatus

import pytest
from fastapi import testclient

from fintrack.app import app

client = testclient.TestClient(app)


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


def test_posting_valid_user_returns_status_created(valid_create_user_request):
    response = client.post("/users", json=valid_create_user_request)
    assert response.status_code == HTTPStatus.CREATED


def test_posting_user_with_invalid_email_returns_status_unprocessable_entity(
    invalid_email_create_user_request,
):
    response = client.post("/users", json=invalid_email_create_user_request)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_created_user_is_returned_without_password(valid_create_user_request):
    response = client.post("/users", json=valid_create_user_request)
    assert "password" not in response.json()
