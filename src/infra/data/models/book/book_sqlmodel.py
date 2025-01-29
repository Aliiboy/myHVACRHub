from uuid import UUID

from sqlmodel import Field, SQLModel

from domain.entities.book.book_entity import Book


class BookSQLModel(SQLModel, table=True):
    __tablename__ = "book"

    id: UUID = Field(primary_key=True)
    title: str
    author: str

    def to_entity(self) -> Book:
        return Book(id=self.id, title=self.title, author=self.author)
