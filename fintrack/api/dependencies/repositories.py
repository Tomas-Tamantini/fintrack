from fintrack.domain.repositories.user_repository import UserRepository
from fintrack.persistence.user_repository import InMemoryUserRepository

in_memory_user_repository = InMemoryUserRepository()


def get_user_repository() -> UserRepository:
    return in_memory_user_repository
