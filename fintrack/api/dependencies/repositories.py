from typing import Annotated

from fastapi import Depends

from fintrack.domain.repositories.user_repository import UserRepository


def get_user_repository() -> UserRepository:
    raise NotImplementedError()


T_UserRepository = Annotated[UserRepository, Depends(get_user_repository)]
