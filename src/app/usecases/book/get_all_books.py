from domain.entities.book.book_entity import Book
from infra.data.repositories.book.book_interface import BookRepositoryInterface


class GetAllBooksUseCase:
    def __init__(self, repository: BookRepositoryInterface):
        self.repository = repository

    def execute(self) -> list[Book]:
        return self.repository.get_all_books()
