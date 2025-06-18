from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from fintrack.api.authentication.jwt import JWTService, TokenPair
from fintrack.api.authentication.password_handler import PasswordHandler
from fintrack.api.dependencies.authentication import (
    get_jwt_service,
    get_password_handler,
)
from fintrack.api.dependencies.repositories import get_user_repository
from fintrack.domain.repositories.user_repository import UserRepository

auth_router = APIRouter(prefix="/auth", tags=["authentication"])


@auth_router.post("/token", response_model=TokenPair)
def get_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_repository: UserRepository = Depends(get_user_repository),
    password_handler: PasswordHandler = Depends(get_password_handler),
    jwt_service: JWTService = Depends(get_jwt_service),
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
