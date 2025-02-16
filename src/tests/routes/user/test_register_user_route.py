from http import HTTPStatus

from sqlalchemy import text

from tests.routes.base_api_test import BaseAPITest


class UserSignUpRouteTests(BaseAPITest):
    def setUp(self) -> None:
        super().setUp()
        self.valid_user = {"email": "test@example.com", "password": "Password_1234!"}
        self.user_with_invalid_password = {
            "email": "test@example.com",
            "password": "password!",
        }

    def tearDown(self) -> None:
        super().tearDown()
        self.session.execute(text("DELETE FROM users"))
        self.session.commit()

    def test_sign_up_user_successfully(self) -> None:
        response = self.client.post("/v1/auth/register", json=self.valid_user)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_sign_up_user_with_duplicate_email_raises_exception(self) -> None:
        self.client.post("/v1/auth/register", json=self.valid_user)
        response = self.client.post("/v1/auth/register", json=self.valid_user)
        self.assertEqual(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

    def test_sign_up_user_with_invalid_password_raises_exception(self) -> None:
        response = self.client.post(
            "/v1/auth/register", json=self.user_with_invalid_password
        )
        self.assertEqual(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
