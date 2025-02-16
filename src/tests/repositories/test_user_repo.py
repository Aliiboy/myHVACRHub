from sqlalchemy import text

from domain.entities.user.user_entity import User
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
        self.valid_user = User(email="test@example.com", password="Password_1234!")

    def tearDown(self) -> None:
        with self.database.get_session() as session:
            session.execute(text("DELETE FROM users"))
            session.commit()
        super().tearDown()

    # add_user
    def test_add_user_success(self) -> None:
        added_user = self.user_repository.add_user(self.valid_user)

        self.assertEqual(self.valid_user.email, added_user.email)
        self.assertNotEqual(self.valid_user.password, added_user.password)
        self.assertTrue(
            self.password_hasher.verify(self.valid_user.password, added_user.password)
        )

    def test_add_user_duplicate_email_raises_exception(self) -> None:
        self.user_repository.add_user(self.valid_user)

        with self.assertRaises(UserDBException):
            self.user_repository.add_user(self.valid_user)

    # get_user_by_email
    def test_get_user_by_email_returns_existing_user(self) -> None:
        user = User(email="test@example.com", password="Password_1234!")
        self.user_repository.add_user(user)
        retrieved_user = self.user_repository.get_user_by_email("test@example.com")
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.email, user.email)  # type: ignore[union-attr]

    def test_get_user_by_email_returns_none_for_nonexistent_user(self) -> None:
        retrieved_user = self.user_repository.get_user_by_email(
            "nonexistent@example.com"
        )
        self.assertIsNone(retrieved_user)

    # get_all_users
    def test_get_all_users_return_all_users_when_users_exist(self) -> None:
        users_to_add: list[User] = [
            User(
                email="user@example.com",
                password="Password_1234!",
            ),
            User(
                email="user2@example.com",
                password="Password_1234!",
            ),
        ]
        for user in users_to_add:
            self.user_repository.add_user(user)

        retrieved_users = self.user_repository.get_all_users(limit=100)
        self.assertEqual(len(users_to_add), len(retrieved_users))
