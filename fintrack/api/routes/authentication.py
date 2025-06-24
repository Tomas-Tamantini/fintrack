from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from fintrack.api.authentication.jwt import TokenPair
from fintrack.api.dependencies.authentication import (
    T_JWTService,
    T_PasswordHandler,
)
from fintrack.api.dependencies.repositories import T_UserRepository

auth_router = APIRouter(prefix="/auth", tags=["authentication"])

T_OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@auth_router.post("/token", response_model=TokenPair)
def get_token(
    form_data: T_OAuth2Form,
    user_repository: T_UserRepository,
    password_handler: T_PasswordHandler,
    jwt_service: T_JWTService,
):
    user = user_repository.get_by_email(form_data.username)
    if not user or not password_handler.verify(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect email or password.",
        )
    return jwt_service.create_token_pair(user_id=user.email)
