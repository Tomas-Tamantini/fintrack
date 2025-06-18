from pwdlib import PasswordHash

from fintrack.api.authentication.password_handler import PasswordHandler


def get_password_handler() -> PasswordHandler:
    return PasswordHash.recommended()
