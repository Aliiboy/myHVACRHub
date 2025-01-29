from abc import ABC, abstractmethod

from domain.entities.book.book_entity import Book


class BookRepositoryInterface(ABC):
    @abstractmethod
    def add_book(self, book: Book) -> Book:
        pass

    @abstractmethod
    def get_all_books(self) -> list[Book]:
        pass
