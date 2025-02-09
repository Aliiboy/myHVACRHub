from app.repositories.book_interface import (
    BookRepositoryInterface,
)
from domain.entities.book.book_entity import Book


class CreateBookUseCase:
    def __init__(self, repository: BookRepositoryInterface):
        self.repository = repository

    def execute(self, title: str, author: str) -> Book:
        new_book = Book(title=title, author=author)

        self.repository.add_book(new_book)
        return new_book
