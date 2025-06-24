from typing import Annotated

from fastapi import Depends
from pwdlib import PasswordHash

from fintrack.api.authentication.jwt import JWTService
from fintrack.api.authentication.password_handler import PasswordHandler


def get_password_handler() -> PasswordHandler:
    return PasswordHash.recommended()


T_PasswordHandler = Annotated[PasswordHandler, Depends(get_password_handler)]


def get_jwt_service() -> JWTService:
    raise NotImplementedError()


T_JWTService = Annotated[JWTService, Depends(get_jwt_service)]
