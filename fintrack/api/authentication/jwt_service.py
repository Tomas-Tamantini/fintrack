from jwt import encode
from pydantic import BaseModel


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class JWTService:
    def __init__(self, key: str, algorithm: str) -> None:
        self._key = key
        self._algorithm = algorithm

    def create_token_pair(self, user_id: str) -> TokenPair:
        data = {"sub": user_id}
        access_token = encode(data, self._key, algorithm=self._algorithm)
        return TokenPair(
            access_token=access_token,
            refresh_token=access_token,
            token_type="Bearer",
        )
