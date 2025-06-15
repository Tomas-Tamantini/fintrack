from typing import Annotated

from fastapi import Depends

from fintrack.api.authentication.password_handler import PasswordHandler


def get_password_handler() -> PasswordHandler:
    raise NotImplementedError()  # TODO: Implement


T_PasswordHandler = Annotated[PasswordHandler, Depends(get_password_handler)]
