from http import HTTPStatus

from fastapi import FastAPI

from fintrack.api.dto.user import CreateUserRequest, CreateUserResponse

app = FastAPI()


@app.post(
    "/users", status_code=HTTPStatus.CREATED, response_model=CreateUserResponse
)
async def create_user(user: CreateUserRequest):
    return CreateUserResponse(
        username=user.username,
        email=user.email,
    )
