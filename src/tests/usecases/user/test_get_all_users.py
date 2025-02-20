import unittest
from typing import cast
from unittest.mock import MagicMock

from app.repositories.user_interface import UserRepositoryInterface
from app.usecases.user.get_all_users import GetAllUsersUsecase
from domain.entities.user.user_entity import UserEntity


class GetAllUsersUsecaseTest(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_user_repository: MagicMock = MagicMock(spec=UserRepositoryInterface)
        self.use_case: GetAllUsersUsecase = GetAllUsersUsecase(
            repository=self.mock_user_repository,
        )

    def test_get_all_users_returns_empty_list_when_no_users_list(self) -> None:
        cast(
            MagicMock, self.mock_user_repository.get_all_users_with_limit
        ).return_value = []

        result: list[UserEntity] = self.use_case.execute(limit=100)

        self.assertEqual(result, [])
        cast(
            MagicMock, self.mock_user_repository.get_all_users_with_limit
        ).assert_called_once()

    def test_get_all_users_return_all_users_when_users_exist(self) -> None:
        users: list[UserEntity] = [
            UserEntity(
                email="user@example.com",
                password="Password_1234!",
            ),
            UserEntity(
                email="user2@example.com",
                password="Password_1234!",
            ),
        ]
        cast(
            MagicMock, self.mock_user_repository.get_all_users_with_limit
        ).return_value = users
        result: list[UserEntity] = self.use_case.execute(limit=100)
        self.assertEqual(len(result), len(users))
