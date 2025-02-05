# src/tests/usecases/user/test_authenticate_user.py
import unittest
from unittest.mock import MagicMock

from app.usecases.user.authenticate_user import AuthenticateUserUseCase
from domain.entities.user.user_entity import User
from domain.services.password_hasher_interface import PasswordHasherInterface
from domain.services.token_service_interface import TokenServiceInterface
from infra.data.repositories.user.user_interface import UserRepositoryInterface


class AuthenticateUserUseCaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_user_repository: MagicMock = MagicMock(spec=UserRepositoryInterface)
        self.mock_password_hasher: MagicMock = MagicMock(spec=PasswordHasherInterface)
        self.mock_token_service: MagicMock = MagicMock(spec=TokenServiceInterface)
        self.use_case: AuthenticateUserUseCase = AuthenticateUserUseCase(
            repository=self.mock_user_repository,
            password_hasher=self.mock_password_hasher,
            token_service=self.mock_token_service,
        )

    def test_authenticate_user_success_returns_valid_token(self) -> None:
        email: str = "test@example.com"
        password: str = "SecurePass123!"
        hashed_password: str = "hashedpassword123"

        # Création d'un utilisateur simulé
        user: User = User(email=email, hashed_password=hashed_password)
        self.mock_user_repository.get_user_by_email.return_value = user

        # Le hasher vérifie correctement le mot de passe
        self.mock_password_hasher.verify.return_value = True
        # Le service de token renvoie un token simulé
        expected_token: str = "token123"
        self.mock_token_service.generate_token.return_value = expected_token

        token: str = self.use_case.execute(email=email, password=password)
        self.assertEqual(token, expected_token)

        self.mock_user_repository.get_user_by_email.assert_called_once_with(email)
        self.mock_password_hasher.verify.assert_called_once_with(
            password, hashed_password
        )
        self.mock_token_service.generate_token.assert_called_once()

    def test_authenticate_user_invalid_email_raises_error(self) -> None:
        email: str = "nonexistent@example.com"
        password: str = "SecurePass123!"
        self.mock_user_repository.get_user_by_email.return_value = None

        with self.assertRaises(ValueError) as context:
            self.use_case.execute(email=email, password=password)
        self.assertEqual(str(context.exception), "Email incorrect.")

    def test_authenticate_user_invalid_password_raises_error(self) -> None:
        email: str = "test@example.com"
        password: str = "WrongPass"
        hashed_password: str = "hashedpassword123"
        user: User = User(email=email, hashed_password=hashed_password)
        self.mock_user_repository.get_user_by_email.return_value = user

        self.mock_password_hasher.verify.return_value = False

        with self.assertRaises(ValueError) as context:
            self.use_case.execute(email=email, password=password)
        self.assertEqual(str(context.exception), "Mot de passe incorrect.")
