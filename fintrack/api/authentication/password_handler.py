from typing import Protocol


class PasswordHandler(Protocol):
    def hash(self, password: str) -> str: ...

    def verify(self, password: str, hash: str) -> bool: ...
