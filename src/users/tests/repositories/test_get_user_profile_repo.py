from uuid import UUID, uuid4

from common.tests.repositories.test_base_repo import TestBaseRepository
from users.domain.entities.user_entity import UserEntity
from users.domain.exceptions.user_exceptions import UserDBException
from users.infra.data.repositories.user_sqlrepo import UserSQLRepository


class TestGetUserProfileSQLRepository(TestBaseRepository):
    """Test de la récupération du profil d'un utilisateur

    Args:
        BaseRepositoryTest (BaseRepositoryTest): Testeur de base pour les tests des répositories
    """

    def setUp(self) -> None:
        """Initialise le testeur de récupération du profil d'un utilisateur

        Returns:
            None
        """
        super().setUp()
        self.user_repository = UserSQLRepository(
            unit_of_work=self.uow, password_hasher=self.password_hasher
        )
        self.valid_user = UserEntity(
            email="test@example.com", password="SecurePassword_1234!"
        )

    def test_get_profile_successfully(self) -> None:
        """Test de la récupération du profil d'un utilisateur

        Returns:
            None
        """
        self.user_repository.sign_up_user(self.valid_user)

        user_profile = self.user_repository.get_user_profile(self.valid_user.id)
        self.assertEqual(self.valid_user.id, user_profile.id)

    def test_get_profile_with_wrong_id(self) -> None:
        """Test de la récupération du profil d'un utilisateur avec un id invalide

        Returns:
            None
        """
        with self.assertRaises(UserDBException) as context:
            wrong_id: UUID = uuid4()
            self.user_repository.get_user_profile(wrong_id)

        expected_message = (
            f"UserException : L'utilisateur avec l'id '{wrong_id}' n'existe pas."
        )
        self.assertIsInstance(context.exception, UserDBException)
        self.assertEqual(str(context.exception), expected_message)
