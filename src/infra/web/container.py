from dependency_injector import containers, providers

from app.usecases.book.create_book import CreateBookUseCase
from app.usecases.book.get_all_books import GetAllBooksUseCase
from app.usecases.humid_air.get_full_ha_props import GetFullHAPropertyUseCase
from infra.data.database import Database
from infra.data.repositories.book.book_sqlrepo import BookSQLRepository
from infra.web.settings import AppSettings


class AppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "infra.web.api.v1.routes.book_routes",
            "infra.web.api.v1.routes.humid_air_routes",
        ]
    )

    # database
    app_settings = providers.Singleton(AppSettings)

    database = providers.Singleton(Database, settings=app_settings)
    database_session = providers.Factory(database.provided.get_session)

    # === book module ===
    # repositories
    book_repository = providers.Factory(
        BookSQLRepository, session_factory=database_session
    )

    # usecases
    create_book_usecase = providers.Factory(
        CreateBookUseCase, repository=book_repository
    )
    get_all_books_usecase = providers.Factory(
        GetAllBooksUseCase, repository=book_repository
    )

    # === humid air module ===
    # repositories
    # usecases
    get_full_ha_props_usecase = providers.Factory(GetFullHAPropertyUseCase)
