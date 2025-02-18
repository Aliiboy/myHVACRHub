# src/tests/usecases/user/test_authenticate_user.py
import unittest
from typing import cast
from unittest.mock import MagicMock

from app.repositories.user_interface import UserRepositoryInterface
from app.schemas.user_schema import UserLoginSchema
from app.usecases.user.login_user import UserLoginUseCase
from domain.exceptions.user_exceptions import UserValidationException
from domain.services.token_service_interface import TokenServiceInterface


class LoginUserUseCaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_user_repository: MagicMock = MagicMock(spec=UserRepositoryInterface)
        self.mock_token_service: MagicMock = MagicMock(spec=TokenServiceInterface)
        self.use_case: UserLoginUseCase = UserLoginUseCase(
            repository=self.mock_user_repository,
            token_service=self.mock_token_service,
        )

    def test_login_user_success_returns_valid_token(self) -> None:
        user_login_valid_schema = UserLoginSchema(
            email="test@example.com", password="Password_1234!"
        )
        self.use_case.execute(user_login_valid_schema)
        cast(MagicMock, self.mock_user_repository.login_user).assert_called_once()
        cast(MagicMock, self.mock_token_service.generate_token).assert_called_once()

    def test_login_user_invalid_data_raises_exception(self) -> None:
        user_login_invalid_schema = UserLoginSchema(
            email="invalid-email", password="123"
        )

        with self.assertRaises(UserValidationException) as context:
            self.use_case.execute(user_login_invalid_schema)

        self.assertIsInstance(context.exception, UserValidationException)
        self.assertTrue(len(context.exception.errors) > 0)
        self.assertEqual(context.exception.errors[0]["field"], "email")
        self.assertEqual(context.exception.errors[1]["field"], "password")
