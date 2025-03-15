import unittest
from typing import cast
from unittest.mock import MagicMock

from users.app.repositories.user_interface import UserRepositoryInterface
from users.app.schemas.user_schema import UserSignUpSchema
from users.app.usecases.sign_up_user import UserSignUpUseCase
from users.domain.entities.user_entity import UserEntity
from users.domain.exceptions.user_exceptions import UserValidationException


class TestUserSignUpUseCase(unittest.TestCase):
    """Test de l'inscription d'un utilisateur

    Args:
        unittest (unittest.TestCase): Testeur de base pour les tests des usecases
    """

    def setUp(self) -> None:
        """Initialise le testeur de l'inscription d'un utilisateur

        Returns:
            None
        """
        self.mock_user_repository: UserRepositoryInterface = MagicMock(
            spec=UserRepositoryInterface
        )
        self.use_case = UserSignUpUseCase(
            repository=self.mock_user_repository,
        )

    def test_signup_user_success(self) -> None:
        """Test de l'inscription d'un utilisateur avec succès

        Returns:
            None
        """

        # Arrange - Préparer les données de test et le comportement attendu
        user_sign_up_schema = UserSignUpSchema(
            email="test@example.com", password="Password_1234!"
        )

        # Configurer le mock pour retourner une entité utilisateur avec l'ID spécifié
        mock_user_entity = UserEntity(
            email=user_sign_up_schema.email, password=user_sign_up_schema.password
        )
        cast(
            MagicMock, self.mock_user_repository.sign_up_user
        ).return_value = mock_user_entity

        # Act - Exécuter le cas d'utilisation
        result = self.use_case.execute(user_sign_up_schema)

        # Assert - Vérifier les résultats et comportements attendus
        cast(MagicMock, self.mock_user_repository.sign_up_user).assert_called_once()
        self.assertEqual(result.email, user_sign_up_schema.email)
        self.assertEqual(result.password, user_sign_up_schema.password)

    def test_signup_user_with_validation_error(self) -> None:
        """Test de l'inscription d'un utilisateur avec des données invalides

        Returns:
            None
        """
        invalid_user_schema = UserSignUpSchema(email="invalid-email", password="123")

        with self.assertRaises(UserValidationException) as context:
            self.use_case.execute(invalid_user_schema)

        self.assertIsInstance(context.exception, UserValidationException)
        self.assertTrue(len(context.exception.errors) > 0)
        self.assertEqual(context.exception.errors[0]["field"], "email")
        self.assertEqual(context.exception.errors[1]["field"], "password")
