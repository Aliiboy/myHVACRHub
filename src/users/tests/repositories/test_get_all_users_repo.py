from common.tests.repositories.test_base_repo import TestBaseRepository
from users.domain.entities.user_entity import UserEntity
from users.infra.data.repositories.user_sqlrepo import UserSQLRepository


class TestGetAllUsersSQLRepository(TestBaseRepository):
    """Test de la récupération de tous les utilisateurs

    Args:
        BaseRepositoryTest (BaseRepositoryTest): Testeur de base pour les tests des répositories
    """

    def setUp(self) -> None:
        super().setUp()
        self.user_repository = UserSQLRepository(
            unit_of_work=self.uow, password_hasher=self.password_hasher
        )
        self.users_to_add: list[UserEntity] = [
            UserEntity(
                email="user@example.com",
                password="Password_1234!",
            ),
            UserEntity(
                email="user2@example.com",
                password="Password_1234!",
            ),
        ]

    def test_get_all_users_return_all_users_when_users_exist(self) -> None:
        """Test de la récupération de tous les utilisateurs

        Returns:
            None
        """
        for user in self.users_to_add:
            self.user_repository.sign_up_user(user)

        retrieved_users = self.user_repository.get_all_users_with_limit(limit=100)
        self.assertEqual(len(self.users_to_add), len(retrieved_users))
