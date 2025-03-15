from http import HTTPStatus

from sqlalchemy import text

from common.tests.routes.test_base_api import TestBaseAPI


class TestGetAllUsersRoute(TestBaseAPI):
    """Test de la récupération de tous les utilisateurs

    Args:
        BaseAPITest (BaseAPITest): Testeur de base pour les tests des routes
    """

    def setUp(self) -> None:
        """Initialise le testeur de récupération de tous les utilisateurs

        Returns:
            None
        """
        super().setUp()
        self.admin_data = {
            "email": "admin@example.com",
            "password": "SecurePass123!",
        }
        self.client.post("/v1/auth/sign_up", json=self.admin_data)

        self.session.execute(
            text("UPDATE users SET role='ADMIN' WHERE email='admin@example.com'")
        )
        self.session.commit()

    def test_get_all_users_return_all_users_when_users_exist(self) -> None:
        """Test de la récupération de tous les utilisateurs

        Returns:
            None
        """
        login_response = self.client.post("/v1/auth/login", json=self.admin_data)
        self.assertEqual(login_response.status_code, HTTPStatus.OK)
        token = login_response.get_json()["access_token"]

        user_1 = {"email": "user1@example.com", "password": "SecurePass123!"}
        user_2 = {"email": "user2@example.com", "password": "SecurePass123!"}
        self.client.post("/v1/auth/sign_up", json=user_1)
        self.client.post("/v1/auth/sign_up", json=user_2)

        response = self.client.get(
            "/v1/auth/get_all_users?limit=100",
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        response_data = response.get_json()
        self.assertIn("users", response_data)
        self.assertEqual(len(response_data["users"]), 3)
