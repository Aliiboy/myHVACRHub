import unittest
from typing import cast
from unittest.mock import MagicMock
from uuid import uuid4

from users.app.repositories.user_interface import UserRepositoryInterface
from users.app.usecases.delete_user import DeleteUserByIdUsecase


class TestDeleteUserByIdUsecase(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_user_repository: MagicMock = MagicMock(spec=UserRepositoryInterface)
        self.use_case: DeleteUserByIdUsecase = DeleteUserByIdUsecase(
            repository=self.mock_user_repository,
        )

    def test_delete_user_success(self) -> None:
        self.use_case.execute(uuid4())
        cast(
            MagicMock, self.mock_user_repository.delete_user_by_id
        ).assert_called_once()
