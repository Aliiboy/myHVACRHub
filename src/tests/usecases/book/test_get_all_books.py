import unittest
from unittest.mock import MagicMock

from app.usecases.book.get_all_books import GetAllBooksUseCase
from domain.entities.book.book_entity import Book
from infra.data.repositories.book.interface import BookRepositoryInterface


class TestGetAllBooksUseCase(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_repository = MagicMock(spec=BookRepositoryInterface)
        self.use_case = GetAllBooksUseCase(repository=self.mock_repository)

    def test_get_all_books_with_empty_repository(self) -> None:
        # given
        self.mock_repository.get_all_books.return_value = []
        # when
        result = self.use_case.execute()
        # then
        self.assertEqual(result, [])
        self.mock_repository.get_all_books.assert_called_once()

    def test_get_all_books_with_multiple_books(self) -> None:
        # given
        books = [
            Book(title="Book 1", author="Author 1"),
            Book(title="Book 2", author="Author 2"),
        ]
        self.mock_repository.get_all_books.return_value = books
        # when
        result = self.use_case.execute()
        # then
        self.assertEqual(len(result), len(books))
        for i, book in enumerate(result):
            self.assertEqual(book.title, books[i].title)
            self.assertEqual(book.author, books[i].author)
        self.mock_repository.get_all_books.assert_called_once()
