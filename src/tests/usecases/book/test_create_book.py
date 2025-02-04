import unittest
from typing import cast
from unittest.mock import MagicMock

from app.usecases.book.create_book import CreateBookUseCase
from domain.entities.book.book_entity import Book
from domain.settings.book_settings import BookEntitieSettings
from infra.data.repositories.book.book_interface import BookRepositoryInterface


class CreateBookUseCaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_repository: BookRepositoryInterface = MagicMock(
            spec=BookRepositoryInterface
        )
        self.use_case = CreateBookUseCase(repository=self.mock_repository)

    def test_create_book_with_invalid_title_raises_value_error(self) -> None:
        invalid_title: str = "a" * (BookEntitieSettings.title_max_length + 1)
        author: str = "Douglas Adams"

        with self.assertRaises(ValueError):
            self.use_case.execute(title=invalid_title, author=author)

    def test_create_book_with_valid_data_returns_book_entity(self) -> None:
        valid_title: str = "Le guide du voyageur galactique"
        valid_author: str = "Douglas Adams"

        created_book: Book = self.use_case.execute(
            title=valid_title, author=valid_author
        )

        self.assertIsInstance(created_book, Book)
        self.assertEqual(created_book.title, valid_title)
        self.assertEqual(created_book.author, valid_author)
        cast(MagicMock, self.mock_repository.add_book).assert_called_once_with(
            created_book
        )
