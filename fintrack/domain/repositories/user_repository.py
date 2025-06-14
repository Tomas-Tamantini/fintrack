from typing import Protocol

from fintrack.domain.models.user import User, UserCore


class UserRepository(Protocol):
    def create(self, user: UserCore) -> User: ...
