from uuid import UUID, uuid4

from common.tests.repositories.test_base_repo import TestBaseRepository
from users.domain.entities.user_entity import UserEntity
from users.domain.exceptions.user_exceptions import UserDBException
from users.infra.data.repositories.user_sqlrepo import UserSQLRepository


class TestDeleteUserByIdSQLRepository(TestBaseRepository):
    """Test de la suppression d'un utilisateur par son id

    Args:
        BaseRepositoryTest (BaseRepositoryTest): Testeur de base pour les tests des répositories
    """

    def setUp(self) -> None:
        """Initialise le testeur de suppression d'un utilisateur par son id

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

    def test_delete_user_by_id_success(self) -> None:
        """Test de la suppression d'un utilisateur par son id

        Returns:
            None
        """
        user_to_delete = self.user_repository.sign_up_user(self.valid_user)
        self.user_repository.delete_user_by_id(user_to_delete.id)
        users_after = self.user_repository.get_all_users_with_limit(limit=100)
        self.assertNotIn(user_to_delete.email, [user.email for user in users_after])

    def test_delete_user_by_id_with_wrong_id(self) -> None:
        """Test de la suppression d'un utilisateur par son id avec un id invalide

        Returns:
            None
        """
        with self.assertRaises(UserDBException) as context:
            wrong_id: UUID = uuid4()
            self.user_repository.delete_user_by_id(wrong_id)

        expected_message = (
            f"UserException : L'utilisateur avec l'id '{wrong_id}' n'existe pas."
        )
        self.assertIsInstance(context.exception, UserDBException)
        self.assertEqual(str(context.exception), expected_message)
