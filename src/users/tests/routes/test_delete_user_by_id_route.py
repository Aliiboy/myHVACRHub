import uuid
from http import HTTPStatus

from sqlalchemy import text

from common.tests.routes.test_base_api import TestBaseAPI


class TestDeleteUserByIdRoute(TestBaseAPI):
    """Test de la suppression d'un utilisateur par son id

    Args:
        BaseAPITest (BaseAPITest): Testeur de base pour les tests des routes
    """

    def setUp(self) -> None:
        """Initialise le testeur de suppression d'un utilisateur par son id

        Returns:
            None
        """
        super().setUp()
        self.admin_data = {"email": "admin2@example.com", "password": "SecurePass123!"}
        self.client.post("/v1/auth/sign_up", json=self.admin_data)

        self.session.execute(
            text("UPDATE users SET role='ADMIN' WHERE email='admin2@example.com'")
        )
        self.session.commit()

        login_response = self.client.post("/v1/auth/login", json=self.admin_data)
        self.admin_token = login_response.get_json()["access_token"]

    def test_delete_user_by_id_success(self) -> None:
        """Test de la suppression d'un utilisateur par son id

        Returns:
            None
        """
        user_to_delete = {
            "email": "user_to_delete@example.com",
            "password": "Password_1234!",
        }
        response = self.client.post("/v1/auth/sign_up", json=user_to_delete)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

        user_id = self.session.execute(
            text("SELECT id FROM users WHERE email='user_to_delete@example.com'")
        ).scalar()

        if isinstance(user_id, str):
            user_id = uuid.UUID(user_id)

        delete_response = self.client.delete(
            f"/v1/auth/user/{user_id}",
            headers={"Authorization": f"Bearer {self.admin_token}"},
        )

        self.assertEqual(delete_response.status_code, HTTPStatus.OK)
        self.assertEqual(
            delete_response.get_json()["message"], "Utilisateur supprimé avec succès."
        )

    def test_delete_user_by_id_with_wrong_id(self) -> None:
        """Test de la suppression d'un utilisateur par son id avec un id invalide

        Returns:
            None
        """
        wrong_id: uuid.UUID = uuid.uuid4()
        delete_response = self.client.delete(
            f"/v1/auth/user/{wrong_id}",
            headers={"Authorization": f"Bearer {self.admin_token}"},
        )
        self.assertEqual(delete_response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(
            delete_response.get_json()["message"],
            f"UserException : L'utilisateur avec l'id '{wrong_id}' n'existe pas.",
        )
