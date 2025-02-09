import unittest
from http import HTTPStatus
from unittest.mock import patch

from flask import Flask, Response
from flask_jwt_extended import JWTManager, create_access_token

from infra.web.decorators.role_required import role_required
from infra.web.dtos.generic import SuccessResponse


class TestRoleRequiredDecorator(unittest.TestCase):
    def setUp(self) -> None:
        self.app = Flask(__name__)
        self.app.config["JWT_SECRET_KEY"] = "test_secret"
        self.jwt = JWTManager(self.app)

        @self.app.route("/protected")
        @role_required("admin", "moderator")
        def protected() -> Response:
            return SuccessResponse(
                code=HTTPStatus.OK, message="Accès autorisé"
            ).to_response()

        self.client = self.app.test_client()

    def test_access_with_authorized_role(self) -> None:
        with self.app.app_context():
            token = create_access_token(
                identity="user1", additional_claims={"role": "admin"}
            )
            response = self.client.get(
                "/protected", headers={"Authorization": f"Bearer {token}"}
            )
            self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_access_with_unauthorized_role(self) -> None:
        with self.app.app_context():
            token = create_access_token(
                identity="user2", additional_claims={"role": "user"}
            )
            response = self.client.get(
                "/protected", headers={"Authorization": f"Bearer {token}"}
            )
            self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_access_without_role_claim(self) -> None:
        with self.app.app_context():
            token = create_access_token(identity="user3")
            response = self.client.get(
                "/protected", headers={"Authorization": f"Bearer {token}"}
            )
            self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    @patch("infra.web.decorators.role_required.verify_jwt_in_request")
    @patch("infra.web.decorators.role_required.get_jwt", return_value={})
    def test_access_without_jwt(self, mock_get_jwt, mock_verify_jwt) -> None:
        response = self.client.get("/protected")
        self.assertEqual(response.status_code, 403)
