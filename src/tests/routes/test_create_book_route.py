import unittest

from flask.testing import FlaskClient
from flask_openapi3.openapi import OpenAPI
from sqlalchemy import text

from infra.data.database import Database
from infra.web.app import WebApp
from infra.web.container import AppContainer


class TestCreateBookRoutes(unittest.TestCase):
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
        self.session.execute(text("DELETE FROM book"))
        self.session.commit()
        self.context.__exit__(None, None, None)

    def test_create_book(self) -> None:
        # given
        book_data = {
            "title": "Le guide du voyageur galactique",
            "author": "Douglas Adams",
        }
        # when
        response = self.client.post("/v1/book/create_book", json=book_data)
        # then
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertEqual(response_data["title"], book_data["title"])
        self.assertEqual(response_data["author"], book_data["author"])
        self.assertIn("id", response_data)
        self.assertIn("created_at", response_data)

    def test_create_book_with_empty_value(self) -> None:
        # given
        book_data = {
            "title": "",
            "author": "",
        }
        # when
        response = self.client.post("/v1/book/create_book", json=book_data)
        # then
        self.assertEqual(response.status_code, 422)
