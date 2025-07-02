from datetime import datetime, timedelta, timezone

from jwt import encode
from pydantic import BaseModel


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class JWTService:
    def __init__(
        self, key: str, algorithm: str, access_token_duration_minutes: int
    ) -> None:
        self._key = key
        self._algorithm = algorithm
        self._access_token_duration_minutes = access_token_duration_minutes

    def create_token_pair(self, user_id: str) -> TokenPair:
        data = {
            "sub": user_id,
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=self._access_token_duration_minutes),
        }
        access_token = encode(data, self._key, algorithm=self._algorithm)
        return TokenPair(
            access_token=access_token,
            refresh_token=access_token,
            token_type="Bearer",
        )
