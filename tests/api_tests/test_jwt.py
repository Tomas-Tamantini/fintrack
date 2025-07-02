from jwt import decode

from fintrack.api.authentication.jwt_service import JWTService

KEY = "secretkey"
ALGORITHM = "HS256"


def test_jwt_generates_bearer_tokens():
    service = JWTService(KEY, ALGORITHM)
    token_pair = service.create_token_pair("testuser")
    assert token_pair.token_type == "Bearer"


def test_jwt_generates_access_and_refresh_token_with_give_subject():
    service = JWTService(KEY, ALGORITHM)
    token_pair = service.create_token_pair("testuser")
    assert (
        decode(token_pair.access_token, KEY, algorithms=[ALGORITHM])["sub"]
        == "testuser"
    )
