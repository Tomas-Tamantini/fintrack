from pwdlib import PasswordHash

from fintrack.api.authentication.jwt import JWTService
from fintrack.api.authentication.password_handler import PasswordHandler


def get_password_handler() -> PasswordHandler:
    return PasswordHash.recommended()


def get_jwt_service() -> JWTService:
    raise NotImplementedError()
