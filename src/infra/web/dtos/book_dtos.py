from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from domain.entities.book.book_entity import Book
from domain.settings.book_settings import BookEntitieSettings


class BookRequestDTO(BaseModel):
    title: str = Field(
        ...,
        min_length=BookEntitieSettings.title_min_length,
        max_length=BookEntitieSettings.title_max_length,
        description=BookEntitieSettings.title_description,
    )
    author: str = Field(
        ...,
        min_length=BookEntitieSettings.author_min_length,
        max_length=BookEntitieSettings.author_max_length,
        description=BookEntitieSettings.author_decription,
    )


class BookResponseDTO(BaseModel):
    id: UUID = Field()
    title: str = Field()
    author: str = Field()
    created_at: datetime = Field()


class BookListResponseDTO(BaseModel):
    books: list[Book]


class GetAllBooksQueryParams(BaseModel):
    limit: int = Field(default=100, gt=0)
