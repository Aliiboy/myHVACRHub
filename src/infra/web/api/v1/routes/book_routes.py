from typing import Any

from dependency_injector.wiring import Provide, inject
from flask_openapi3 import APIBlueprint, Tag  # type: ignore[attr-defined]

from app.usecases.book.create_book import CreateBookUseCase
from app.usecases.book.get_all_books import GetAllBooksUseCase
from infra.web.container import AppContainer
from infra.web.dtos.book_dtos import (
    BookListResponseDTO,
    BookRequestDTO,
    BookResponseDTO,
    GetAllBooksQueryParams,
)

tag = Tag(name="book", description="Some Book")
router = APIBlueprint(
    "/",
    __name__,
    url_prefix="/book",
    abp_tags=[tag],
    doc_ui=False,
)


@router.post("/create_book", responses={200: BookResponseDTO})
@inject
def create_book(
    body: BookRequestDTO,
    use_case: CreateBookUseCase = Provide[AppContainer.create_book_usecase],
) -> dict[str, Any]:
    new_book = use_case.execute(title=body.title, author=body.author)
    response = BookResponseDTO(
        id=new_book.id,
        title=new_book.title,
        author=new_book.author,
        created_at=new_book.created_at,
    )
    return response.model_dump()


@router.get("/get_all_books", responses={200: BookListResponseDTO})
@inject
def get_all_books(
    query: GetAllBooksQueryParams,
    use_case: GetAllBooksUseCase = Provide[AppContainer.get_all_books_usecase],
) -> dict[str, Any]:
    limit = query.limit
    all_books = use_case.execute()
    limited_books = all_books[:limit]
    response = BookListResponseDTO(books=limited_books)
    return response.model_dump()
