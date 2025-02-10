from http import HTTPStatus

from sqlalchemy import text

from tests.routes.base_api_test import BaseAPITest


class GetColdRoomCoolingLoadFastRouteTests(BaseAPITest):
    def tearDown(self) -> None:
        self.session.execute(text("DELETE FROM users"))
        self.session.commit()
        super().tearDown()

    def test_get_bilan_frigo_ratio_with_valid_data(self) -> None:
        user_data = {
            "email": "user@example.com",
            "password": "SecurePass123!",
        }
        self.client.post("/v1/auth/register", json=user_data)

        login_response = self.client.post("/v1/auth/login", json=user_data)
        self.assertEqual(login_response.status_code, HTTPStatus.OK)
        token = login_response.get_json()["access_token"]

        valid_data = {
            "length": 20,
            "width": 20,
            "height": 4.5,
            "type": "CF",
        }
        response = self.client.get(
            "/v1/fast_quote/get_cold_room_cooling_load_fast",
            query_string=valid_data,
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response_data = response.get_json()

        for key in ["length", "width", "height", "type", "volume", "cooling_load"]:
            self.assertIn(key, response_data)
