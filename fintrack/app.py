from http import HTTPStatus

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class CreateUserRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class CreateUserResponse(BaseModel):
    username: str
    email: EmailStr


@app.post(
    "/users", status_code=HTTPStatus.CREATED, response_model=CreateUserResponse
)
async def create_user(user: CreateUserRequest):
    return CreateUserResponse(
        username=user.username,
        email=user.email,
    )
