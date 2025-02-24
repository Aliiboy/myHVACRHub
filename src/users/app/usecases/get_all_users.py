from users.app.repositories.user_interface import UserRepositoryInterface
from users.domain.entities.user_entity import UserEntity


class GetAllUsersUsecase:
    def __init__(self, repository: UserRepositoryInterface):
        self.repository = repository

    def execute(self, limit: int) -> list[UserEntity]:
        return self.repository.get_all_users_with_limit(limit)
