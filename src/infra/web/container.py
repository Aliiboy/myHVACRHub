from dependency_injector import containers, providers

from app.usecases.humid_air.get_ha_props import GetHumidAirPropertyUseCase
from app.usecases.user.delete_user import DeleteUserByIdUsecase
from app.usecases.user.get_all_users import GetAllUsersUsecase
from app.usecases.user.login_user import UserLoginUseCase
from app.usecases.user.sign_up_user import UserSignUpUseCase
from infra.data.repositories.user_sqlrepo import UserSQLRepository
from infra.data.sql_database import SQLDatabase
from infra.data.sql_unit_of_work import SQLUnitOfWork
from infra.services.bcrypt_password_hasher import BcryptPasswordHasher
from infra.services.jwt_token_service import JWTTokenService
from infra.web.settings import AppSettings


class AppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
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

    # === humid air module ===
    # repositories
    # usecases
    humid_air_usecases = providers.Dict(
        get_ha_props=providers.Factory(GetHumidAirPropertyUseCase)
    )

    # === user module ===
    # repositories
    user_repository = providers.Factory(
        UserSQLRepository, unit_of_work=unit_of_work, password_hasher=password_hasher
    )
    # usecases
    user_usecases = providers.Dict(
        sign_up=providers.Factory(UserSignUpUseCase, repository=user_repository),
        delete_user=providers.Factory(
            DeleteUserByIdUsecase, repository=user_repository
        ),
        login=providers.Factory(
            UserLoginUseCase, repository=user_repository, token_service=token_service
        ),
        get_all_users=providers.Factory(GetAllUsersUsecase, repository=user_repository),
    )
