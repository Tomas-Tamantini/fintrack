from fintrack.domain.models.user import User, UserCore

# TODO: Replace with database-backed repository


class InMemoryUserRepository:
    def __init__(self) -> None:
        self._users = []

    def create(self, user: UserCore) -> User:
        stored = User(
            id=len(self._users) + 1,
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
        )
        self._users.append(stored)
        print(len(self._users), "users stored in memory")
        return stored
