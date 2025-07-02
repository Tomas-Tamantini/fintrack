from typing import Annotated

from fastapi import Depends
from pwdlib import PasswordHash

from fintrack.api.authentication.jwt_service import JWTService
from fintrack.api.authentication.password_handler import PasswordHandler


def get_password_handler() -> PasswordHandler:
    return PasswordHash.recommended()


T_PasswordHandler = Annotated[PasswordHandler, Depends(get_password_handler)]


def get_jwt_service() -> JWTService:
    # TODO: Extract key, expirations and algorithm from .env
    return JWTService(
        key="tempkey",
        algorithm="HS256",
        access_token_duration_minutes=15,
        refresh_token_duration_minutes=30 * 24 * 60,
    )


T_JWTService = Annotated[JWTService, Depends(get_jwt_service)]
