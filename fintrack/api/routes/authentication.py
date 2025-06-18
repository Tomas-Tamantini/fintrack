from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from fintrack.api.authentication.password_handler import PasswordHandler
from fintrack.api.dependencies.authentication import get_password_handler
from fintrack.api.dependencies.repositories import get_user_repository
from fintrack.domain.repositories.user_repository import UserRepository

auth_router = APIRouter(prefix="/auth", tags=["authentication"])


@auth_router.post("/token")
def get_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_repository: UserRepository = Depends(get_user_repository),
    password_handler: PasswordHandler = Depends(get_password_handler),
):
    user = user_repository.get_by_email(form_data.username)
    if not user or not password_handler.verify(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect email or password.",
        )
    raise NotImplementedError()
