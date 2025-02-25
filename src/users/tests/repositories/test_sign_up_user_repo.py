from sqlalchemy import text

from common.tests.repositories.base_repo_test import BaseRepositoryTest
from users.domain.entities.user_entity import UserEntity
from users.domain.exceptions.user_exceptions import UserDBException
from users.infra.data.repositories.user_sqlrepo import UserSQLRepository


class UserSignUpSQLRepositoryTests(BaseRepositoryTest):
    def setUp(self) -> None:
        super().setUp()
        self.user_repository = UserSQLRepository(
            unit_of_work=self.uow, password_hasher=self.password_hasher
        )
        self.valid_user = UserEntity(
            email="test@example.com", password="Password_1234!"
        )

    # def tearDown(self) -> None:
    #     with self.database.get_session() as session:
    #         session.execute(text("DELETE FROM users"))
    #         session.commit()
    #     super().tearDown()

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
