from http import HTTPStatus

from sqlalchemy import text

from common.tests.routes.base_api_test import BaseAPITest


class LoginUserRouteTests(BaseAPITest):
    def setUp(self) -> None:
        super().setUp()
        user_data = {"email": "test@example.com", "password": "SecurePass123!"}
        self.client.post("/v1/auth/sign_up", json=user_data)

    def tearDown(self) -> None:
        super().tearDown()
        self.session.execute(text("DELETE FROM users"))
        self.session.commit()

    def test_login_user_successfully(self) -> None:
        login_data = {"email": "test@example.com", "password": "SecurePass123!"}
        response = self.client.post("/v1/auth/login", json=login_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response_data = response.get_json()
        self.assertIn("access_token", response_data)

    def test_login_with_invalid_password_returns_error(self) -> None:
        login_data = {"email": "test@example.com", "password": "WrongPass"}
        response = self.client.post("/v1/auth/login", json=login_data)
        self.assertEqual(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

    def test_login_with_invalid_email_returns_error(self) -> None:
        login_data = {"email": "nonexistent@example.com", "password": "SecurePass123!"}
        response = self.client.post("/v1/auth/login", json=login_data)
        self.assertEqual(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
