import unittest
from http import HTTPStatus
from unittest.mock import MagicMock, patch

from flask import Flask, Response
from flask_jwt_extended import JWTManager, create_access_token

from common.infra.web.dtos.generic import SuccessResponse
from users.domain.entities.user_entity import UserRole
from users.infra.web.decorators.role_required import role_required


class TestRoleRequiredDecorator(unittest.TestCase):
    """Test du décorateur role_required

    Args:
        unittest (unittest.TestCase): Testeur de décorateur
    """

    def setUp(self) -> None:
        """Initialise le testeur de décorateur

        Returns:
            None
        """
        self.app = Flask(__name__)
        self.app.config["JWT_SECRET_KEY"] = "test_secret"
        self.jwt = JWTManager(self.app)

        @self.app.route("/protected")
        @role_required(UserRole.ADMIN, UserRole.MODERATOR)
        def protected() -> Response:
            """Route protégée par le décorateur role_required

            Returns:
                Response: Réponse de succès
            """
            return SuccessResponse(
                code=HTTPStatus.OK, message="Accès autorisé"
            ).to_response()

        self.client = self.app.test_client()

    def test_access_with_authorized_role(self) -> None:
        """Test d'accès avec un rôle autorisé

        Returns:
            None
        """
        with self.app.app_context():
            token = create_access_token(
                identity="user1", additional_claims={"role": "ADMIN"}
            )
            response = self.client.get(
                "/protected", headers={"Authorization": f"Bearer {token}"}
            )
            self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_access_with_unauthorized_role(self) -> None:
        """Test d'accès avec un rôle non autorisé

        Returns:
            None
        """
        with self.app.app_context():
            token = create_access_token(
                identity="user2", additional_claims={"role": "USER"}
            )
            response = self.client.get(
                "/protected", headers={"Authorization": f"Bearer {token}"}
            )
            self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_access_without_role_claim(self) -> None:
        """Test d'accès sans le rôle dans le jeton

        Returns:
            None
        """
        with self.app.app_context():
            token = create_access_token(identity="user3")
            response = self.client.get(
                "/protected", headers={"Authorization": f"Bearer {token}"}
            )
            self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    @patch("users.infra.web.decorators.role_required.verify_jwt_in_request")
    @patch("users.infra.web.decorators.role_required.get_jwt", return_value={})
    def test_access_without_jwt(
        self, mock_get_jwt: MagicMock, mock_verify_jwt: MagicMock
    ) -> None:
        """Test d'accès sans le jeton

        Returns:
            None
        """
        response = self.client.get("/protected")
        self.assertEqual(response.status_code, 403)
