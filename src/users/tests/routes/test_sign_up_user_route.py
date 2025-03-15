from http import HTTPStatus

from common.tests.routes.test_base_api import TestBaseAPI


class TestUserSignUpRoute(TestBaseAPI):
    """Test de l'inscription d'un utilisateur

    Args:
        BaseAPITest (BaseAPITest): Testeur de base pour les tests des routes
    """

    def setUp(self) -> None:
        """Initialise le testeur de l'inscription d'un utilisateur

        Returns:
            None
        """
        super().setUp()
        self.valid_user = {"email": "test@example.com", "password": "Password_1234!"}
        self.user_with_invalid_password = {
            "email": "test@example.com",
            "password": "pass",
        }

    def test_sign_up_user_successfully(self) -> None:
        """Test de l'inscription d'un utilisateur avec succès

        Returns:
            None
        """
        response = self.client.post("/v1/auth/sign_up", json=self.valid_user)
        print(response.get_json())
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(
            response.get_json()["message"], "Utilisateur créé avec succès."
        )

    def test_sign_up_user_with_duplicate_email_raises_exception(self) -> None:
        """Test de l'inscription d'un utilisateur avec un email déjà utilisé

        Returns:
            None
        """
        self.client.post("/v1/auth/sign_up", json=self.valid_user)
        response = self.client.post("/v1/auth/sign_up", json=self.valid_user)
        self.assertEqual(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        self.assertEqual(
            response.get_json()["message"],
            "UserException : L'utilisateur avec l'email 'test@example.com' existe déjà.",
        )
