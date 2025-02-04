from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from domain.entities.user.user_entity import User
from infra.data.repositories.user.user_sqlrepo import UserSQLRepository
from tests.repositories.base_repo_test import BaseRepositoryTest


class UserSQLRepositoryTests(BaseRepositoryTest):
    def setUp(self) -> None:
        super().setUp()
        self.user_repository = UserSQLRepository(uow=self.uow)

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
        with self.assertRaises(IntegrityError):
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
