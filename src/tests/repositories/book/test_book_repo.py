import unittest
from typing import ClassVar
from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from domain.entities.book.book_entity import Book
from infra.data.database import Database
from infra.data.repositories.book.book_sqlrepo import BookSQLRepository
from infra.web.settings import AppSettings


class TestSQLRepository(unittest.TestCase):
    database: ClassVar[Database]

    @classmethod
    def setUpClass(cls) -> None:
        settings = AppSettings(DATABASE_URL="sqlite:///:memory:", DATABASE_ECHO=False)
        cls.database = Database(settings=settings)
        cls.database.create_database()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.database.engine.dispose()

    def setUp(self) -> None:
        self.context = self.database.get_session()
        self.session = self.context.__enter__()
        self.repository = BookSQLRepository(
            session_factory=lambda: self.database.get_session()
        )

    def tearDown(self) -> None:
        self.session.execute(text("DELETE FROM book"))
        self.session.commit()
        self.context.__exit__(None, None, None)

    def test_add_book(self) -> None:
        # given
        new_book = Book(title="Le guide du voyageur galactique", author="Douglas Adams")
        # when
        added_book = self.repository.add_book(new_book)
        # then
        self.assertEqual(added_book.id, new_book.id)

    def test_add_book_integrity_error(self) -> None:
        # given
        book1 = Book(
            id=uuid4(), title="Le guide du voyageur galactique", author="Douglas Adams"
        )
        book2 = Book(
            id=book1.id, title="Son odeur aprés la pluie", author="Cédric Sapin-Defour"
        )
        # when
        self.repository.add_book(book1)
        # then
        with self.assertRaises(IntegrityError):
            self.repository.add_book(book2)

    def test_get_all_books(self) -> None:
        # given
        books = [
            Book(id=uuid4(), title="Book 1", author="Author 1"),
            Book(id=uuid4(), title="Book 2", author="Author 2"),
        ]
        for book in books:
            self.repository.add_book(book)
        # when
        retrieved_books = self.repository.get_all_books()
        # then
        self.assertEqual(len(retrieved_books), len(books))
        for original, retrieved in zip(books, retrieved_books, strict=True):
            self.assertEqual(original.id, retrieved.id)
            self.assertEqual(original.title, retrieved.title)
            self.assertEqual(original.author, retrieved.author)
