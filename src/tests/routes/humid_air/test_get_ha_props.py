import unittest

from flask.testing import FlaskClient
from flask_openapi3.openapi import OpenAPI

from infra.data.database import Database
from infra.web.app import WebApp
from infra.web.container import AppContainer


class TestGetHAPropsRoutes(unittest.TestCase):
    web_app: OpenAPI
    client: FlaskClient
    database: Database

    @classmethod
    def setUpClass(cls) -> None:
        container = AppContainer()
        container.init_resources()
        cls.web_app = WebApp(container=container).app
        cls.client = cls.web_app.test_client()
        cls.database = container.database()

    def setUp(self) -> None:
        self.context = self.database.get_session()
        self.session = self.context.__enter__()

    def tearDown(self) -> None:
        self.context.__exit__(None, None, None)

    def test_get_ha_props_valid_data(self) -> None:
        # given
        ha_data = {
            "pressure": 101325,
            "temp_dry_bulb": 25.0,
            "relative_humidity": 50.0,
        }
        # when
        response = self.client.get("/v1/humid_air/get_ha_props", query_string=ha_data)
        # then
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertIn("pressure", response_data)
        self.assertIn("temp_dry_bulb", response_data)
        self.assertIn("relative_humidity", response_data)

    def test_get_ha_props_invalid_data(self) -> None:
        # given
        ha_data = {
            "pressure": 101325,
            "temp_dry_bulb": 345.0,
            "relative_humidity": 50.0,
        }
        # when
        response = self.client.get("/v1/humid_air/get_ha_props", query_string=ha_data)
        # then
        self.assertEqual(response.status_code, 422)
        response_data = response.get_json()
        self.assertIn("code", response_data)
        self.assertEqual(response_data["code"], 422)
        self.assertIn("message", response_data)
