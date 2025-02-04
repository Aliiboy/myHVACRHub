import unittest
from datetime import datetime, timedelta
from uuid import UUID

from domain.entities.book.book_entity import Book
from domain.settings.book_settings import BookEntitieSettings


class TestBookId(unittest.TestCase):
    def test_book_id_is_generated(self) -> None:
        valid_book = Book(
            title="Le guide du voyageur galactique",
            author="Douglas Adams",
        )
        self.assertIsInstance(valid_book.id, UUID)

    def test_book_id_is_unique(self) -> None:
        valid_book_1 = Book(
            title="Le guide du voyageur galactique",
            author="Douglas Adams",
        )
        valid_book_2 = Book(
            title="Le guide du voyageur galactique",
            author="Douglas Adams",
        )
        self.assertNotEqual(valid_book_1.id, valid_book_2.id)


class TestBookTitle(unittest.TestCase):
    def test_book_title_is_too_long(self) -> None:
        long_title = "A" * (BookEntitieSettings.title_max_length + 1)
        with self.assertRaises(ValueError):
            Book(title=long_title, author="Douglas Adams")


class TestBookDuration(unittest.TestCase):
    def test_book_valid_duration(self) -> None:
        book = Book(
            title="Le guide du voyageur galactique",
            author="Douglas Adams",
            created_at=datetime.utcnow() - timedelta(days=10),
        )
        self.assertEqual(book.duration_in_days, 10)
