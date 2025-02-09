from app.repositories.user_interface import UserRepositoryInterface
from domain.entities.user.user_entity import User


class GetAllUsersUsecase:
    def __init__(self, repository: UserRepositoryInterface):
        self.repository = repository

    def execute(self, limit: int) -> list[User]:
        return self.repository.get_all_users(limit)
