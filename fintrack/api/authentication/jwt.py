from pydantic import BaseModel


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class JWTService:
    def create_token_pair(self, user_id: str) -> TokenPair:
        raise NotImplementedError("JWT token creation not implemented.")
