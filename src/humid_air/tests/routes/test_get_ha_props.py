from http import HTTPStatus

from common.tests.routes.test_base_api import TestBaseAPI


class TestHumidAirRoutes(TestBaseAPI):
    def test_get_humid_air_properties_with_valid_data(self) -> None:
        valid_data = {
            "pressure": 101325,
            "temp_dry_bulb": 25.0,
            "relative_humidity": 50.0,
        }
        response = self.client.get(
            "/v1/humid_air/get_ha_props", query_string=valid_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response_data = response.get_json()
        self.assertIn("pressure", response_data)
        self.assertIn("temp_dry_bulb", response_data)
        self.assertIn("relative_humidity", response_data)

    def test_get_humid_air_properties_with_invalid_data_returns_error(self) -> None:
        invalid_data = {
            "pressure": 101325,
            "temp_dry_bulb": 345.0,
            "relative_humidity": 50.0,
        }
        response = self.client.get(
            "/v1/humid_air/get_ha_props", query_string=invalid_data
        )
        self.assertEqual(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        response_data = response.get_json()
        self.assertIn("code", response_data)
        self.assertEqual(response_data["code"], HTTPStatus.UNPROCESSABLE_ENTITY)
        self.assertIn("message", response_data)
