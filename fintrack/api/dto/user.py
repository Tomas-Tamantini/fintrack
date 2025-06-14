from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class CreateUserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
