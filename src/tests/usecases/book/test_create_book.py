import unittest
from unittest.mock import MagicMock

from app.usecases.book.create_book import CreateBookUseCase
from domain.settings.book_settings import BookEntitieSettings
from infra.data.repositories.book.interface import BookRepositoryInterface


class TestCreateBookUseCase(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_repository = MagicMock(spec=BookRepositoryInterface)
        self.use_case = CreateBookUseCase(repository=self.mock_repository)

    def test_create_book_with_invalid_title(self) -> None:
        # given
        invalid_title: str = "a" * (BookEntitieSettings.title_max_length + 1)
        author: str = "Douglas Adams"
        # when
        with self.assertRaises(ValueError):
            self.use_case.execute(title=invalid_title, author=author)
        # then

    def test_create_book_with_valid_data(self) -> None:
        title: str = "Le guide du voyageur galactique"
        author: str = "Douglas Adams"
        # when
        book = self.use_case.execute(title=title, author=author)
        # then
        self.assertEqual(book.title, title)
        self.assertEqual(book.author, author)
        self.mock_repository.add_book.assert_called_once_with(book)
