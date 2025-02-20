from uuid import UUID

from app.repositories.user_interface import UserRepositoryInterface


class DeleteUserByIdUsecase:
    def __init__(self, repository: UserRepositoryInterface):
        self.repository = repository

    def execute(self, user_id: UUID) -> None:
        return self.repository.delete_user_by_id(user_id)
