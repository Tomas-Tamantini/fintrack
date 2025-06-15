from typing import Protocol


class PasswordHandler(Protocol):
    def hash(self, password: str) -> str: ...
