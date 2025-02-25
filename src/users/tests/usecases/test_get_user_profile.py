import unittest
from typing import cast
from unittest.mock import MagicMock
from uuid import uuid4

from users.app.repositories.user_interface import UserRepositoryInterface
from users.app.usecases.get_user_profile import GetUserProfileUseCase


class GetUserProfileUseCaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_user_repository: MagicMock = MagicMock(spec=UserRepositoryInterface)
        self.use_case: GetUserProfileUseCase = GetUserProfileUseCase(
            repository=self.mock_user_repository,
        )

    def test_get_user_profile_successfully(self) -> None:
        self.use_case.execute(uuid4())
        cast(MagicMock, self.mock_user_repository.get_user_profile).assert_called_once()
