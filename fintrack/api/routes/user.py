from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from fintrack.api.authentication.password_handler import PasswordHandler
from fintrack.api.dependencies.authentication import get_password_handler
from fintrack.api.dependencies.repositories import get_user_repository
from fintrack.api.dto.user import CreateUserRequest, CreateUserResponse
from fintrack.domain.exceptions import ConflictError
from fintrack.domain.models.user import UserCore
from fintrack.domain.repositories.user_repository import UserRepository

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.post(
    "/", status_code=HTTPStatus.CREATED, response_model=CreateUserResponse
)
def create_user(
    user: CreateUserRequest,
    repository: UserRepository = Depends(get_user_repository),
    password_handler: PasswordHandler = Depends(get_password_handler),
) -> CreateUserResponse:
    parsed = UserCore(
        username=user.username,
        email=user.email,
        hashed_password=password_handler.hash(user.password),
    )
    try:
        stored = repository.create(parsed)
        return CreateUserResponse(
            id=stored.id, username=stored.username, email=stored.email
        )
    except ConflictError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="User with this username or email already exists.",
        )
