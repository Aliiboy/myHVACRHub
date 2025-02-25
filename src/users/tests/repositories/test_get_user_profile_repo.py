from uuid import UUID, uuid4

from common.tests.repositories.base_repo_test import BaseRepositoryTest
from users.domain.entities.user_entity import UserEntity
from users.domain.exceptions.user_exceptions import UserDBException
from users.infra.data.repositories.user_sqlrepo import UserSQLRepository


class GetUserProfileSQLRepositoryTests(BaseRepositoryTest):
    def setUp(self) -> None:
        super().setUp()
        self.user_repository = UserSQLRepository(
            unit_of_work=self.uow, password_hasher=self.password_hasher
        )
        self.valid_user = UserEntity(
            email="test@example.com", password="SecurePassword_1234!"
        )

    def test_get_profile_successfully(self) -> None:
        self.user_repository.sign_up_user(self.valid_user)

        user_profile = self.user_repository.get_user_profile(self.valid_user.id)
        self.assertEqual(self.valid_user.id, user_profile.id)

    def test_get_profile_with_wrong_id(self) -> None:
        with self.assertRaises(UserDBException) as context:
            wrong_id: UUID = uuid4()
            self.user_repository.get_user_profile(wrong_id)

        expected_message = (
            f"UserDBException : L'utilisateur avec l'id '{wrong_id}' n'existe pas."
        )
        self.assertIsInstance(context.exception, UserDBException)
        self.assertEqual(str(context.exception), expected_message)
