import unittest
from typing import cast
from unittest.mock import MagicMock

import bcrypt

from app.usecases.user.create_user import CreateUserUseCase
from domain.entities.user.user_entity import User
from infra.data.repositories.user.user_interface import UserRepositoryInterface
from infra.services.bcrypt_password_hasher import BcryptPasswordHasher


class CreateUserUseCaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_user_repository: UserRepositoryInterface = MagicMock(
            spec=UserRepositoryInterface
        )
        self.mock_password_hasher = BcryptPasswordHasher()
        self.use_case = CreateUserUseCase(
            repository=self.mock_user_repository,
            password_hasher=self.mock_password_hasher,
        )

    def test_create_user_success(self) -> None:
        email: str = "test@example.com"
        password: str = "SecurePass123!"
        cast(MagicMock, self.mock_user_repository.get_user_by_email).return_value = None

        new_user: User = self.use_case.execute(email=email, password=password)

        self.assertIsInstance(new_user, User)
        self.assertEqual(new_user.email, email)
        self.assertTrue(
            bcrypt.checkpw(password.encode(), new_user.hashed_password.encode())
        )
        cast(MagicMock, self.mock_user_repository.add_user).assert_called_once_with(
            new_user
        )

    def test_create_user_with_existing_email_raises_error(self) -> None:
        existing_user: User = User(
            email="test@example.com", hashed_password="hashedpwd"
        )
        cast(
            MagicMock, self.mock_user_repository.get_user_by_email
        ).return_value = existing_user

        with self.assertRaises(ValueError) as context:
            self.use_case.execute(email="test@example.com", password="SecurePass123!")
        self.assertEqual(str(context.exception), "L'email est déjà utilisé.")
