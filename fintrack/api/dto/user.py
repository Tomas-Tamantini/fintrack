from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel, str_strip_whitespace=True):
    username: str
    email: EmailStr
    password: str


class CreateUserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
