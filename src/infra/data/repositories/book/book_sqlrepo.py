from collections.abc import Callable
from contextlib import AbstractContextManager

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from domain.entities.book.book_entity import Book
from infra.data.models.book.book_sqlmodel import BookSQLModel
from infra.data.repositories.book.book_interface import BookRepositoryInterface


class BookSQLRepository(BookRepositoryInterface):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory

    def add_book(self, book: Book) -> Book:
        with self.session_factory() as session:
            query = BookSQLModel(id=book.id, title=book.title, author=book.author)
            try:
                session.add(query)
                session.commit()
                session.refresh(query)
                return query.to_entity()
            except IntegrityError as e:
                session.rollback()
                raise e

    def get_all_books(self) -> list[Book]:
        with self.session_factory() as session:
            query = session.exec(
                select(BookSQLModel)
            ).all()  # Updated to use session.exec
            return [book.to_entity() for book in query]
