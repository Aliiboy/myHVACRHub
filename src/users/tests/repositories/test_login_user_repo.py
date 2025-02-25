from sqlalchemy import text

from common.tests.repositories.base_repo_test import BaseRepositoryTest
from users.domain.entities.user_entity import UserEntity
from users.domain.exceptions.user_exceptions import UserDBException
from users.infra.data.repositories.user_sqlrepo import UserSQLRepository


class UserLoginSQLRepositoryTests(BaseRepositoryTest):
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

    # def tearDown(self) -> None:
    #     with self.database.get_session() as session:
    #         session.execute(text("DELETE FROM users"))
    #         session.commit()
    #     super().tearDown()

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
