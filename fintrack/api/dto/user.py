from pydantic import BaseModel, EmailStr, Field


class CreateUserRequest(BaseModel, str_strip_whitespace=True):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str


class CreateUserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
