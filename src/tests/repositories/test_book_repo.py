from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from domain.entities.book.book_entity import Book
from infra.data.repositories.book_sqlrepo import BookSQLRepository
from tests.repositories.base_repo_test import BaseRepositoryTest


class BookSQLRepositoryTests(BaseRepositoryTest):
    def setUp(self) -> None:
        super().setUp()
        self.book_repository = BookSQLRepository(unit_of_work=self.uow)

    def tearDown(self) -> None:
        with self.database.get_session() as session:
            session.execute(text("DELETE FROM books"))
            session.commit()
        super().tearDown()

    def test_add_book_successfully(self) -> None:
        new_book = Book(title="Le guide du voyageur galactique", author="Douglas Adams")
        added_book = self.book_repository.add_book(new_book)
        self.assertEqual(added_book.id, new_book.id)
        self.assertEqual(added_book.title, new_book.title)
        self.assertEqual(added_book.author, new_book.author)

    def test_add_book_duplicate_id_raises_integrity_error(self) -> None:
        book1 = Book(title="Le guide du voyageur galactique", author="Douglas Adams")
        book2 = Book(title="Le guide du voyageur galactique", author="Douglas Adams")
        self.book_repository.add_book(book1)
        with self.assertRaises(IntegrityError):
            self.book_repository.add_book(book2)

    def test_get_all_books_returns_all_books(self) -> None:
        books_to_add = [
            Book(title="Book 1", author="Author 1"),
            Book(title="Book 2", author="Author 2"),
        ]
        for book in books_to_add:
            self.book_repository.add_book(book)
        retrieved_books = self.book_repository.get_all_books()

        self.assertEqual(len(retrieved_books), len(books_to_add))
        for original, retrieved in zip(books_to_add, retrieved_books, strict=False):
            self.assertEqual(original.title, retrieved.title)
            self.assertEqual(original.author, retrieved.author)
