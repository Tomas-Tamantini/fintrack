from datetime import datetime, timezone

import pytest
from freezegun import freeze_time
from jwt import decode

from fintrack.api.authentication.jwt_service import JWTService, TokenType

KEY = "secretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION_MINUTES = 15
REFRESH_TOKEN_EXPIRATION_MINUTES = 120


@pytest.fixture
def service():
    return JWTService(
        KEY,
        ALGORITHM,
        ACCESS_TOKEN_EXPIRATION_MINUTES,
        REFRESH_TOKEN_EXPIRATION_MINUTES,
    )


@pytest.fixture
def decoded_access_token(service):
    def _decoded_access_token(user_id: str = "testuser"):
        token_pair = service.create_token_pair(user_id)
        return decode(token_pair.access_token, KEY, algorithms=[ALGORITHM])

    return _decoded_access_token


@pytest.fixture
def decoded_refresh_token(service):
    def _decoded_refresh_token(user_id: str = "testuser"):
        token_pair = service.create_token_pair(user_id)
        return decode(
            token_pair.refresh_token,
            KEY,
            algorithms=[ALGORITHM],
            options={"verify_nbf": False},
        )

    return _decoded_refresh_token


def test_jwt_generates_bearer_tokens(service):
    token_pair = service.create_token_pair("testuser")
    assert token_pair.auth_scheme == "Bearer"


def test_jwt_generates_access_token_with_given_subject(decoded_access_token):
    access_token = decoded_access_token("testuser")
    assert access_token["sub"] == "testuser"


def test_jwt_generates_access_token_with_proper_token_type(
    decoded_access_token,
):
    access_token = decoded_access_token()
    assert access_token["token_type"] == TokenType.ACCESS


def test_jwt_generates_access_token_with_given_expiration(
    decoded_access_token,
):
    with freeze_time("2023-01-01 12:00:00"):
        access_token = decoded_access_token()
        expiration = datetime.fromtimestamp(
            access_token["exp"], tz=timezone.utc
        )
        assert expiration == datetime(2023, 1, 1, 12, 15, tzinfo=timezone.utc)


def test_jwt_generates_refresh_token_with_given_subject(decoded_refresh_token):
    refresh_token = decoded_refresh_token("testuser")
    assert refresh_token["sub"] == "testuser"


def test_jwt_generates_refresh_token_with_proper_token_type(
    decoded_refresh_token,
):
    refresh_token = decoded_refresh_token()
    assert refresh_token["token_type"] == TokenType.REFRESH


def test_jwt_generates_refresh_token_with_given_expiration(
    decoded_refresh_token,
):
    with freeze_time("2023-01-01 12:00:00"):
        refresh_token = decoded_refresh_token()
        expiration = datetime.fromtimestamp(
            refresh_token["exp"], tz=timezone.utc
        )
        assert expiration == datetime(2023, 1, 1, 14, 15, tzinfo=timezone.utc)


def test_jwt_generates_refresh_token_with_given_nbf(decoded_refresh_token):
    with freeze_time("2023-01-01 12:00:00"):
        refresh_token = decoded_refresh_token()
        not_before = datetime.fromtimestamp(
            refresh_token["nbf"], tz=timezone.utc
        )
        assert not_before == datetime(2023, 1, 1, 12, 15, tzinfo=timezone.utc)
