from http import HTTPStatus

from common.tests.routes.base_api_test import BaseAPITest


class GetUserProfileRouteTests(BaseAPITest):
    def setUp(self) -> None:
        super().setUp()
        self.valid_user = {
            "email": "user@example.com",
            "password": "SecurePass123!",
        }
        self.client.post("/v1/auth/sign_up", json=self.valid_user)
        self.login_response = self.client.post("/v1/auth/login", json=self.valid_user)
        self.token = self.login_response.get_json()["access_token"]

    def test_get_user_profile_successfully(self) -> None:
        self.assertEqual(self.login_response.status_code, HTTPStatus.OK)

        response = self.client.get(
            "/v1/auth/profile", headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.get_json()["email"], "user@example.com")
        self.assertEqual(response.get_json()["role"], "user")

    def test_get_user_profile_with_wrong_id(self) -> None:
        wrong_id = "c5de7e9e-6b7b-43c1-8e8e-9997806e25b4"
        response = self.client.get(
            "/v1/auth/profile",
            headers={
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjNWRlN2U5ZS02YjdiLTQzYzEtOGU4ZS05OTk3ODA2ZTI1YjQiLCJyb2xlIjoidXNlciJ9.KCZW1IZSAEEQg1gd1h3UEkPODh_5advtJJzcfTJSTyo"
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(
            response.get_json()["message"],
            f"UserDBException : L'utilisateur avec l'id '{wrong_id}' n'existe pas.",
        )
