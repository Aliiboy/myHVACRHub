import unittest
from typing import cast
from unittest.mock import MagicMock

from app.usecases.book.get_all_books import GetAllBooksUseCase
from domain.entities.book.book_entity import Book
from infra.data.repositories.book.book_interface import BookRepositoryInterface


class GetAllBooksUseCaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_repository: BookRepositoryInterface = MagicMock(
            spec=BookRepositoryInterface
        )
        self.use_case = GetAllBooksUseCase(repository=self.mock_repository)

    def test_get_all_books_returns_empty_list_when_no_books_exist(self) -> None:
        cast(MagicMock, self.mock_repository.get_all_books).return_value = []

        result: list[Book] = self.use_case.execute()

        self.assertEqual(result, [])
        cast(MagicMock, self.mock_repository.get_all_books).assert_called_once()

    def test_get_all_books_returns_all_books_when_books_exist(self) -> None:
        books: list[Book] = [
            Book(title="Book 1", author="Author 1"),
            Book(title="Book 2", author="Author 2"),
        ]
        cast(MagicMock, self.mock_repository.get_all_books).return_value = books

        result: list[Book] = self.use_case.execute()

        self.assertEqual(len(result), len(books))
        for expected, actual in zip(books, result, strict=False):
            self.assertEqual(expected.title, actual.title)
            self.assertEqual(expected.author, actual.author)
        cast(MagicMock, self.mock_repository.get_all_books).assert_called_once()
