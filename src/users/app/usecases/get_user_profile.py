from uuid import UUID

from users.app.repositories.user_interface import UserRepositoryInterface
from users.domain.entities.user_entity import UserEntity


class GetUserProfileUseCase:
    def __init__(self, repository: UserRepositoryInterface):
        self.repository = repository

    def execute(self, user_id: UUID) -> UserEntity:
        return self.repository.get_user_profile(user_id)
