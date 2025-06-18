from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from fintrack.api.dependencies.authentication import T_PasswordHandler
from fintrack.api.dependencies.repositories import T_UserRepository
from fintrack.api.dto.user import CreateUserRequest, CreateUserResponse
from fintrack.domain.exceptions import ConflictError
from fintrack.domain.models.user import UserCore

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.post(
    "/", status_code=HTTPStatus.CREATED, response_model=CreateUserResponse
)
def create_user(
    user: CreateUserRequest,
    repository: T_UserRepository,
    password_handler: T_PasswordHandler,
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
