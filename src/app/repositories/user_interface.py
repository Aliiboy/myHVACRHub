from abc import ABC, abstractmethod

from domain.entities.user.user_entity import UserEntity


class UserRepositoryInterface(ABC):
    # write
    @abstractmethod
    def sign_up_user(self, schema: UserEntity) -> UserEntity:
        pass

    # read
    @abstractmethod
    def login_user(self, schema: UserEntity) -> UserEntity:
        pass

    @abstractmethod
    def get_all_users(self, limit: int) -> list[UserEntity]:
        pass
