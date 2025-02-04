from sqlalchemy import text

from tests.routes.base_api_test import BaseAPITest


class TestCreateBookRoutes(BaseAPITest):
    def tearDown(self) -> None:
        self.session.execute(text("DELETE FROM books"))
        self.session.commit()
        super().tearDown()

    def test_create_book(self) -> None:
        book_data = {
            "title": "Le guide du voyageur galactique",
            "author": "Douglas Adams",
        }
        response = self.client.post("/v1/book/create_book", json=book_data)
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertEqual(response_data["title"], book_data["title"])
        self.assertEqual(response_data["author"], book_data["author"])
        self.assertIn("id", response_data)
        self.assertIn("created_at", response_data)

    def test_create_book_with_empty_value(self) -> None:
        book_data = {
            "title": "",
            "author": "",
        }
        response = self.client.post("/v1/book/create_book", json=book_data)
        self.assertEqual(response.status_code, 422)
