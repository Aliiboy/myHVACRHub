from sqlmodel import select

from app.repositories.book_interface import BookRepositoryInterface
from domain.entities.book.book_entity import Book
from infra.data.models.book_sqlmodel import BookSQLModel
from infra.data.sql_unit_of_work import SQLUnitOfWork


class BookSQLRepository(BookRepositoryInterface):
    def __init__(self, uow: SQLUnitOfWork):
        self.uow = uow

    def add_book(self, book: Book) -> Book:
        with self.uow as uow:
            query = BookSQLModel(
                id=book.id,
                title=book.title,
                author=book.author,
            )
            uow.session.add(query)
            uow.session.flush()
            return query.to_entity()

    def get_all_books(self) -> list[Book]:
        with self.uow as uow:
            query = uow.session.exec(select(BookSQLModel)).all()
            return [book.to_entity() for book in query]
