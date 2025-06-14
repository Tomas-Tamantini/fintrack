from http import HTTPStatus

from fastapi import APIRouter

from fintrack.api.dto.user import CreateUserRequest, CreateUserResponse

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.post(
    "/", status_code=HTTPStatus.CREATED, response_model=CreateUserResponse
)
def create_user(user: CreateUserRequest) -> CreateUserResponse:
    return CreateUserResponse(id=1, username=user.username, email=user.email)
