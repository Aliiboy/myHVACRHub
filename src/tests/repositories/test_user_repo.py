from uuid import UUID, uuid4

from sqlalchemy import text

from domain.entities.user.user_entity import UserEntity
from domain.exceptions.user_exceptions import (
    UserDBException,
)
from infra.data.repositories.user_sqlrepo import UserSQLRepository
from tests.repositories.base_repo_test import BaseRepositoryTest


class UserSQLRepositoryTests(BaseRepositoryTest):
    def setUp(self) -> None:
        super().setUp()
        self.user_repository = UserSQLRepository(
            unit_of_work=self.uow, password_hasher=self.password_hasher
        )
        self.valid_user = UserEntity(
            email="test@example.com", password="Password_1234!"
        )
        self.invalid_user = UserEntity(
            email="test@example.com", password="WrongPassword_1234!"
        )
        self.invalid_user_email = UserEntity(
            email="test2@example.com", password="Password_1234!"
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

    def tearDown(self) -> None:
        with self.database.get_session() as session:
            session.execute(text("DELETE FROM users"))
            session.commit()
        super().tearDown()

    # sign_up_user
    def test_sign_up_user_success(self) -> None:
        added_user = self.user_repository.sign_up_user(self.valid_user)

        self.assertEqual(self.valid_user.email, added_user.email)
        self.assertNotEqual(self.valid_user.password, added_user.password)
        self.assertTrue(
            self.password_hasher.verify(self.valid_user.password, added_user.password)
        )

    def test_sign_up_user_duplicate_email_raises_exception(self) -> None:
        self.user_repository.sign_up_user(self.valid_user)

        with self.assertRaises(UserDBException):
            self.user_repository.sign_up_user(self.valid_user)

    # delete_user
    def test_delete_user_by_id_success(self) -> None:
        user_to_delete = self.user_repository.sign_up_user(self.valid_user)
        self.user_repository.delete_user_by_id(user_to_delete.id)
        users_after = self.user_repository.get_all_users_with_limit(limit=100)
        self.assertNotIn(user_to_delete.email, [user.email for user in users_after])

    def test_delete_user_by_id_with_wrong_id(self) -> None:
        with self.assertRaises(UserDBException) as context:
            wrong_id: UUID = uuid4()
            self.user_repository.delete_user_by_id(wrong_id)

        expected_message = (
            f"UserDBException : L'utilisateur avec l'id '{wrong_id}' n'existe pas."
        )
        self.assertIsInstance(context.exception, UserDBException)
        self.assertEqual(str(context.exception), expected_message)

    # login_user
    def test_login_user_success(self) -> None:
        self.user_repository.sign_up_user(self.valid_user)

        user_to_login = self.user_repository.login_user(self.valid_user)
        self.assertEqual(self.valid_user.email, user_to_login.email)
        self.assertTrue(
            self.password_hasher.verify(
                self.valid_user.password, user_to_login.password
            )
        )

    def test_login_user_with_wrong_password(self) -> None:
        self.user_repository.sign_up_user(self.valid_user)

        with self.assertRaises(UserDBException):
            self.user_repository.login_user(self.invalid_user)

    def test_login_user_with_invalid_email(self) -> None:
        self.user_repository.sign_up_user(self.valid_user)

        with self.assertRaises(UserDBException):
            self.user_repository.login_user(self.invalid_user_email)

    # get_all_users
    def test_get_all_users_return_all_users_when_users_exist(self) -> None:
        for user in self.users_to_add:
            self.user_repository.sign_up_user(user)

        retrieved_users = self.user_repository.get_all_users_with_limit(limit=100)
        self.assertEqual(len(self.users_to_add), len(retrieved_users))
