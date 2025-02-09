from sqlalchemy import text

from domain.entities.user.user_entity import User
from domain.exceptions.user_exceptions import UserAlreadyExistsException
from infra.data.repositories.user_sqlrepo import UserSQLRepository
from tests.repositories.base_repo_test import BaseRepositoryTest


class UserSQLRepositoryTests(BaseRepositoryTest):
    def setUp(self) -> None:
        super().setUp()
        self.user_repository = UserSQLRepository(unit_of_work=self.uow)

    def tearDown(self) -> None:
        with self.database.get_session() as session:
            session.execute(text("DELETE FROM users"))
            session.commit()
        super().tearDown()

    def test_add_user_successfully(self) -> None:
        user = User(email="test@example.com", hashed_password="hashedpassword123")
        added_user = self.user_repository.add_user(user)
        self.assertEqual(added_user.id, user.id)
        self.assertEqual(added_user.email, user.email)
        self.assertEqual(added_user.hashed_password, user.hashed_password)

    def test_add_user_duplicate_email_raises_integrity_error(self) -> None:
        user1 = User(email="test@example.com", hashed_password="hashedpassword123")
        user2 = User(email="test@example.com", hashed_password="anotherpassword")
        self.user_repository.add_user(user1)
        with self.assertRaises(UserAlreadyExistsException):
            self.user_repository.add_user(user2)

    def test_get_user_by_email_returns_existing_user(self) -> None:
        user = User(email="test@example.com", hashed_password="hashedpassword123")
        self.user_repository.add_user(user)
        retrieved_user = self.user_repository.get_user_by_email("test@example.com")
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user, user)

    def test_get_user_by_email_returns_none_for_nonexistent_user(self) -> None:
        retrieved_user = self.user_repository.get_user_by_email(
            "nonexistent@example.com"
        )
        self.assertIsNone(retrieved_user)

    def test_get_all_users_return_all_users_when_users_exist(self) -> None:
        users_to_add: list[User] = [
            User(
                email="user@example.com",
                hashed_password="hash_password",
            ),
            User(
                email="user2@example.com",
                hashed_password="hash_password",
            ),
        ]
        for user in users_to_add:
            self.user_repository.add_user(user)

        retrieved_users = self.user_repository.get_all_users(limit=100)
        self.assertEqual(len(users_to_add), len(retrieved_users))
