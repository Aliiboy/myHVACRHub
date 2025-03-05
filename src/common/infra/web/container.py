from dependency_injector import containers, providers

from common.infra.data.sql_database import SQLDatabase
from common.infra.data.sql_unit_of_work import SQLUnitOfWork
from common.infra.web.settings import AppSettings
from humid_air.app.usecases.get_ha_props import GetHumidAirPropertyUseCase
from users.app.usecases.delete_user import DeleteUserByIdUsecase
from users.app.usecases.get_all_users import GetAllUsersUsecase
from users.app.usecases.get_user_profile import GetUserProfileUseCase
from users.app.usecases.login_user import UserLoginUseCase
from users.app.usecases.sign_up_user import UserSignUpUseCase
from users.infra.data.repositories.user_sqlrepo import UserSQLRepository
from users.infra.services.bcrypt_password_hasher import BcryptPasswordHasher
from users.infra.services.jwt_token_service import JWTTokenService


class AppContainer(containers.DeclarativeContainer):
    """Conteneur de l'application

    Args:
        containers (containers.DeclarativeContainer): Conteneur de dépendances
    """

    wiring_config = containers.WiringConfiguration(
        modules=[
            "humid_air.infra.web.api.v1.humid_air_routes",
            "users.infra.web.api.v1.user_routes",
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
        get_user_profile=providers.Factory(
            GetUserProfileUseCase, repository=user_repository
        ),
        get_all_users=providers.Factory(GetAllUsersUsecase, repository=user_repository),
    )
