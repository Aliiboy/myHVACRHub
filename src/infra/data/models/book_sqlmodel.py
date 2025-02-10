from uuid import UUID

from sqlmodel import Field, SQLModel

from domain.entities.book.book_entity import Book
from domain.settings.book_settings import BookEntitieSettings


class BookSQLModel(SQLModel, table=True):
    __tablename__ = "books"

    id: UUID = Field(primary_key=True)
    title: str = Field(unique=True, index=True)
    author: str = Field()

    def to_entity(self) -> Book:
        return Book(id=self.id, title=self.title, author=self.author)
