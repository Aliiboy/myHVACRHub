import unittest
from datetime import timedelta
from typing import cast
from unittest.mock import MagicMock

import bcrypt
import jwt

from app.usecases.user.authenticate_user import AuthenticateUserUseCase
from domain.entities.user.user_entity import User
from infra.data.repositories.user.user_interface import UserRepositoryInterface
from infra.web.settings import AppSettings


class AuthenticateUserUseCaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_user_repository = MagicMock(spec=UserRepositoryInterface)
        self.mock_app_settings: AppSettings = MagicMock(spec=AppSettings)
        self.mock_app_settings.JWT_SECRET_KEY = "testsecret"
        self.mock_app_settings.JWT_ALGORITHM = "HS256"
        self.mock_app_settings.JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)
        self.use_case = AuthenticateUserUseCase(
            repository=self.mock_user_repository, settings=self.mock_app_settings
        )

    def test_authenticate_user_success_returns_valid_token(self) -> None:
        email: str = "test@example.com"
        password: str = "SecurePass123"
        hashed_password: str = bcrypt.hashpw(
            password.encode(), bcrypt.gensalt()
        ).decode()

        user: User = User(email=email, hashed_password=hashed_password)
        cast(MagicMock, self.mock_user_repository.get_user_by_email).return_value = user

        token: str = self.use_case.execute(email=email, password=password)

        decoded_token = jwt.decode(
            token,
            key=self.mock_app_settings.JWT_SECRET_KEY,
            algorithms=[self.mock_app_settings.JWT_ALGORITHM],
            leeway=10,
        )
        self.assertEqual(decoded_token["sub"], str(user.id))
        self.assertIn("exp", decoded_token)

    def test_authenticate_user_permanent_token_when_no_expiration(self) -> None:
        self.mock_app_settings.JWT_ACCESS_TOKEN_EXPIRES = None
        email: str = "test@example.com"
        password: str = "SecurePass123"
        hashed_password: str = bcrypt.hashpw(
            password.encode(), bcrypt.gensalt()
        ).decode()
        user: User = User(email=email, hashed_password=hashed_password)
        cast(MagicMock, self.mock_user_repository.get_user_by_email).return_value = user

        token: str = self.use_case.execute(email=email, password=password)

        decoded_token = jwt.decode(
            token,
            key=self.mock_app_settings.JWT_SECRET_KEY,
            algorithms=[self.mock_app_settings.JWT_ALGORITHM],
        )
        self.assertEqual(decoded_token["sub"], str(user.id))
        self.assertNotIn("exp", decoded_token)
