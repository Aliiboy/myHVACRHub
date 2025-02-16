from abc import ABC, abstractmethod

from domain.entities.user.user_entity import User


class UserRepositoryInterface(ABC):
    # write
    @abstractmethod
    def add_user(self, schema: User) -> User:
        pass

    # read
    @abstractmethod
    def get_user_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    def get_all_users(self, limit: int) -> list[User]:
        pass
