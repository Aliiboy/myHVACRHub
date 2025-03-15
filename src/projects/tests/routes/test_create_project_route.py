from http import HTTPStatus

from common.tests.routes.test_base_api import TestBaseAPI


class TestCreateProjectRoute(TestBaseAPI):
    """Test de création d'un projet

    Args:
        BaseAPITest (BaseAPITest): Testeur de base pour les tests des routes
    """

    def setUp(self) -> None:
        """Initialise le testeur de création de projet

        Returns:
            None
        """
        super().setUp()
        # Créer un utilisateur pour les tests
        self.user_data = {"email": "test@example.com", "password": "SecurePass123!"}
        self.client.post("/v1/auth/sign_up", json=self.user_data)

        # Se connecter pour obtenir un token
        login_response = self.client.post("/v1/auth/login", json=self.user_data)
        self.token = login_response.get_json()["access_token"]

        # Préparer les données de test
        self.valid_project = {
            "project_number": "PRJ-2024-001",
            "name": "Projet Test",
            "description": "Description du projet de test",
        }

        self.invalid_project = {
            "project_number": "PRJ-2024-001",
            "name": 42,
            "description": "Description du projet de test",
        }

        self.project_with_long_fields = {
            "project_number": "P" * 251,  # Dépasse la longueur maximale de 250
            "name": "N" * 251,  # Dépasse la longueur maximale de 250
            "description": "D" * 251,  # Dépasse la longueur maximale de 250
        }

    def test_create_project_successfully(self) -> None:
        """Test de création d'un projet avec succès

        Returns:
            None
        """
        response = self.client.post(
            "/v1/projects/create_project",
            json=self.valid_project,
            headers={"Authorization": f"Bearer {self.token}"},
        )

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(response.get_json()["message"], "Projet créé avec succès.")

    def test_create_project_without_authentication_returns_error(self) -> None:
        """Test de création d'un projet sans authentification

        Returns:
            None
        """
        response = self.client.post(
            "/v1/projects/create_project",
            json=self.valid_project,
        )

        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_create_project_with_duplicate_number_returns_error(self) -> None:
        """Test de création d'un projet avec un numéro de projet déjà utilisé

        Returns:
            None
        """
        # Crée un premier projet
        self.client.post(
            "/v1/projects/create_project",
            json=self.valid_project,
            headers={"Authorization": f"Bearer {self.token}"},
        )

        # Tente de créer un second projet avec le même numéro
        response = self.client.post(
            "/v1/projects/create_project",
            json=self.valid_project,
            headers={"Authorization": f"Bearer {self.token}"},
        )

        self.assertEqual(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

    def test_create_project_with_fields_too_long_returns_error(self) -> None:
        """Test de création d'un projet avec des champs trop longs

        Returns:
            None
        """
        response = self.client.post(
            "/v1/projects/create_project",
            json=self.project_with_long_fields,
            headers={"Authorization": f"Bearer {self.token}"},
        )

        self.assertEqual(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

    def test_create_project_with_invalid_data_returns_error(self) -> None:
        """Test de création d'un projet avec des données invalides

        Returns:
            None
        """
        response = self.client.post(
            "/v1/projects/create_project",
            json=self.invalid_project,
            headers={"Authorization": f"Bearer {self.token}"},
        )

        self.assertEqual(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
