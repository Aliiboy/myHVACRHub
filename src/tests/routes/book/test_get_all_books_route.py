from sqlalchemy import text

from tests.routes.base_api_test import BaseAPITest


class TestGetAllBooksRoutes(BaseAPITest):
    def tearDown(self) -> None:
        self.session.execute(text("DELETE FROM books"))
        self.session.commit()
        super().tearDown()

    def test_get_all_books(self) -> None:
        book_data_1 = {"title": "Book 1", "author": "Author 1"}
        book_data_2 = {"title": "Book 2", "author": "Author 2"}
        self.client.post("/v1/book/create_book", json=book_data_1)
        self.client.post("/v1/book/create_book", json=book_data_2)
        response = self.client.get("/v1/book/get_all_books")
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertEqual(len(response_data["books"]), 2)
        self.assertEqual(response_data["books"][0]["title"], book_data_1["title"])
        self.assertEqual(response_data["books"][1]["author"], book_data_2["author"])
