import unittest
from typing import cast
from unittest.mock import MagicMock

from users.app.repositories.user_interface import UserRepositoryInterface
from users.app.schemas.user_schema import UserSignUpSchema
from users.app.usecases.sign_up_user import UserSignUpUseCase
from users.domain.exceptions.user_exceptions import UserValidationException


class UserSignUpUseCaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_user_repository: UserRepositoryInterface = MagicMock(
            spec=UserRepositoryInterface
        )
        self.use_case = UserSignUpUseCase(
            repository=self.mock_user_repository,
        )

    def test_signup_user_success(self) -> None:
        user_sign_up_schema = UserSignUpSchema(
            email="test@example.com", password="Password_1234!"
        )

        self.use_case.execute(user_sign_up_schema)
        cast(MagicMock, self.mock_user_repository.sign_up_user).assert_called_once()

    def test_signup_user_with_invalid_data_raises_exception(self) -> None:
        invalid_user_schema = UserSignUpSchema(email="invalid-email", password="123")

        with self.assertRaises(UserValidationException) as context:
            self.use_case.execute(invalid_user_schema)

        self.assertIsInstance(context.exception, UserValidationException)
        self.assertTrue(len(context.exception.errors) > 0)
        self.assertEqual(context.exception.errors[0]["field"], "email")
        self.assertEqual(context.exception.errors[1]["field"], "password")
