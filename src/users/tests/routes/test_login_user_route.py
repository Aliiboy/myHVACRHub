from http import HTTPStatus

from common.tests.routes.test_base_api import TestBaseAPI


class TestLoginUserRoute(TestBaseAPI):
    """Test de la connexion d'un utilisateur

    Args:
        BaseAPITest (BaseAPITest): Testeur de base pour les tests des routes
    """

    def setUp(self) -> None:
        """Initialise le testeur de connexion d'un utilisateur

        Returns:
            None
        """
        super().setUp()
        user_data = {"email": "test@example.com", "password": "SecurePass123!"}
        self.client.post("/v1/auth/sign_up", json=user_data)

    def test_login_user_successfully(self) -> None:
        """Test de la connexion d'un utilisateur avec succès

        Returns:
            None
        """
        login_data = {"email": "test@example.com", "password": "SecurePass123!"}
        response = self.client.post("/v1/auth/login", json=login_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("access_token", response.get_json())

    def test_login_with_invalid_password_returns_error(self) -> None:
        """Test de la connexion d'un utilisateur avec un mot de passe incorrect

        Returns:
            None
        """
        login_data = {"email": "test@example.com", "password": "WrongPass"}
        response = self.client.post("/v1/auth/login", json=login_data)
        self.assertEqual(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        self.assertEqual(response.get_json()["message"][0]["field"], "password")

    def test_login_with_invalid_email_returns_error(self) -> None:
        """Test de la connexion d'un utilisateur avec un email invalide

        Returns:
            None
        """
        login_data = {"email": "nonexistent@example.com", "password": "SecurePass123!"}
        response = self.client.post("/v1/auth/login", json=login_data)
        print(response.get_json())
        self.assertEqual(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        self.assertEqual(
            response.get_json()["message"],
            f"UserException : L'utilisateur avec l'email '{login_data['email']}' n'existe pas.",
        )
