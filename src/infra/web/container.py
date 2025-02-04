from dependency_injector import containers, providers

from app.usecases.book.create_book import CreateBookUseCase
from app.usecases.book.get_all_books import GetAllBooksUseCase
from app.usecases.humid_air.get_full_ha_props import GetFullHAPropertyUseCase
from app.usecases.user.authenticate_user import AuthenticateUserUseCase
from app.usecases.user.create_user import CreateUserUseCase
from infra.data.repositories.book.book_sqlrepo import BookSQLRepository
from infra.data.repositories.user.user_sqlrepo import UserSQLRepository
from infra.data.sql_database import SQLDatabase
from infra.data.sql_unit_of_work import SQLUnitOfWork
from infra.services.bcrypt_password_hasher import BcryptPasswordHasher
from infra.services.jwt_token_service import JWTTokenService
from infra.web.settings import AppSettings


class AppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "infra.web.api.v1.routes.book_routes",
            "infra.web.api.v1.routes.humid_air_routes",
            "infra.web.api.v1.routes.user_routes",
        ]
    )

    app_settings = providers.Singleton(AppSettings)
    # database
    database = providers.Singleton(SQLDatabase, settings=app_settings)
    database_session = providers.Factory(database.provided.get_session)

    # unit of work
    unit_of_work = providers.Factory(SQLUnitOfWork, session_factory=database_session)

    # === services ===
    password_hasher = providers.Factory(BcryptPasswordHasher)
    token_service = providers.Factory(
        JWTTokenService,
        secret_key=app_settings.provided.JWT_SECRET_KEY,
        algorithm=app_settings.provided.JWT_ALGORITHM,
        expires_delta=app_settings.provided.JWT_ACCESS_TOKEN_EXPIRES,
    )

    # === book module ===
    # repositories
    book_repository = providers.Factory(BookSQLRepository, uow=unit_of_work)

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

    # === user module ===
    # repositories
    user_repository = providers.Factory(UserSQLRepository, uow=unit_of_work)
    # usecases
    create_user_usecase = providers.Factory(
        CreateUserUseCase, repository=user_repository, password_hasher=password_hasher
    )
    authenticate_user_usecase = providers.Factory(
        AuthenticateUserUseCase,
        repository=user_repository,
        password_hasher=password_hasher,
        token_service=token_service,
    )
