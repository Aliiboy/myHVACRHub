from http import HTTPStatus

from sqlalchemy import text

from tests.routes.base_api_test import BaseAPITest


class RegisterUserRouteTests(BaseAPITest):
    def tearDown(self) -> None:
        self.session.execute(text("DELETE FROM users"))
        self.session.commit()
        super().tearDown()

    def test_register_user_successfully(self) -> None:
        user_data = {"email": "test@example.com", "password": "SecurePass123!"}
        response = self.client.post("/v1/auth/register", json=user_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_register_user_with_duplicate_email_returns_error(self) -> None:
        user_data = {"email": "test@example.com", "password": "SecurePass123!"}
        self.client.post("/v1/auth/register", json=user_data)
        response = self.client.post("/v1/auth/register", json=user_data)
        self.assertEqual(response.status_code, HTTPStatus.CONFLICT)

    def test_register_user_with_invalid_password_returns_error(self) -> None:
        user_data = {"email": "test3@example.com", "password": "invalidpassword"}
        self.client.post("/v1/auth/register", json=user_data)
        response = self.client.post("/v1/auth/register", json=user_data)
        self.assertEqual(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
