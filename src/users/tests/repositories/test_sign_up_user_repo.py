from common.tests.repositories.test_base_repo import TestBaseRepository
from users.domain.entities.user_entity import UserEntity
from users.domain.exceptions.user_exceptions import UserDBException
from users.infra.data.repositories.user_sqlrepo import UserSQLRepository


class TestUserSignUpSQLRepository(TestBaseRepository):
    """Test de l'inscription d'un utilisateur

    Args:
        BaseRepositoryTest (BaseRepositoryTest): Testeur de base pour les tests des répositories
    """

    def setUp(self) -> None:
        """Initialise le testeur de l'inscription d'un utilisateur

        Returns:
            None
        """
        super().setUp()
        self.user_repository = UserSQLRepository(
            unit_of_work=self.uow, password_hasher=self.password_hasher
        )
        self.valid_user = UserEntity(
            email="test@example.com", password="Password_1234!"
        )

    def test_sign_up_user_success(self) -> None:
        """Test de l'inscription d'un utilisateur

        Returns:
            None
        """
        added_user = self.user_repository.sign_up_user(self.valid_user)

        self.assertEqual(self.valid_user.email, added_user.email)
        self.assertNotEqual(self.valid_user.password, added_user.password)
        self.assertTrue(
            self.password_hasher.verify(self.valid_user.password, added_user.password)
        )

    def test_sign_up_user_duplicate_email_raises_exception(self) -> None:
        """Test de l'inscription d'un utilisateur avec un email déjà utilisé

        Returns:
            None
        """
        self.user_repository.sign_up_user(self.valid_user)

        with self.assertRaises(UserDBException):
            self.user_repository.sign_up_user(self.valid_user)
