from typing import Annotated

from fastapi import Depends

from fintrack.domain.repositories.user_repository import UserRepository
from fintrack.persistence.user_repository import InMemoryUserRepository

in_memory_user_repository = InMemoryUserRepository()


def get_user_repository() -> UserRepository:
    return in_memory_user_repository


T_UserRepository = Annotated[UserRepository, Depends(get_user_repository)]
