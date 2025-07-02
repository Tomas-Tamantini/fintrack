from datetime import datetime, timedelta, timezone

import pytest
from jwt import decode

from fintrack.api.authentication.jwt_service import JWTService

KEY = "secretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION_MINUTES = 15


@pytest.fixture
def service():
    return JWTService(KEY, ALGORITHM, ACCESS_TOKEN_EXPIRATION_MINUTES)


@pytest.fixture
def decoded_access_token(service):
    def _decoded_access_token(user_id: str = "testuser"):
        token_pair = service.create_token_pair(user_id)
        return decode(token_pair.access_token, KEY, algorithms=[ALGORITHM])

    return _decoded_access_token


def test_jwt_generates_bearer_tokens(service):
    token_pair = service.create_token_pair("testuser")
    assert token_pair.token_type == "Bearer"


def test_jwt_generates_access_token_with_given_subject(decoded_access_token):
    access_token = decoded_access_token("testuser")
    assert access_token["sub"] == "testuser"


def test_jwt_generates_access_token_with_given_expiration(
    decoded_access_token,
):
    access_token = decoded_access_token()
    expiration = datetime.fromtimestamp(access_token["exp"], tz=timezone.utc)
    expected_expiration = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRATION_MINUTES
    )
    min_range = expected_expiration - timedelta(seconds=5)
    max_range = expected_expiration + timedelta(seconds=5)
    assert min_range < expiration < max_range


# TODO: Test refresh token sub, nbf and exp
