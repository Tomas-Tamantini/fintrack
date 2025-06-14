from dataclasses import dataclass


@dataclass(frozen=True)
class UserCore:
    username: str
    email: str
    hashed_password: str


@dataclass(frozen=True)
class User(UserCore):
    id: int
