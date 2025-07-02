from datetime import datetime, timedelta, timezone
from enum import Enum

from jwt import encode
from pydantic import BaseModel


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    auth_scheme: str = "Bearer"


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class JWTService:
    def __init__(
        self,
        key: str,
        algorithm: str,
        access_token_duration_minutes: int,
        refresh_token_duration_minutes: int,
    ) -> None:
        self._key = key
        self._algorithm = algorithm
        self._access_token_duration_minutes = access_token_duration_minutes
        self._refresh_token_duration_minutes = refresh_token_duration_minutes

    def _encode(self, data: dict) -> str:
        return encode(data, self._key, algorithm=self._algorithm)

    def create_token_pair(self, user_id: str) -> TokenPair:
        access_token_expiration = datetime.now(timezone.utc) + timedelta(
            minutes=self._access_token_duration_minutes
        )
        refresh_token_expiration = access_token_expiration + timedelta(
            minutes=self._refresh_token_duration_minutes
        )
        access_token_data = {
            "sub": user_id,
            "exp": access_token_expiration,
            "token_type": TokenType.ACCESS,
        }
        refresh_token_data = {
            "sub": user_id,
            "exp": refresh_token_expiration,
            "nbf": access_token_expiration,
            "token_type": TokenType.REFRESH,
        }
        return TokenPair(
            access_token=self._encode(access_token_data),
            refresh_token=self._encode(refresh_token_data),
            auth_scheme="Bearer",
        )
