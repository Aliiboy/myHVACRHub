from dependency_injector import containers, providers

from app.usecases.fast_quote.add_cooling_load_fast_coefficient import (
    AddCoolingLoadFastCoefficientUseCase,
)
from app.usecases.fast_quote.calc_cold_room_cooling_load_fast import (
    CalculateColdRoomCoolingLoadFastUseCase,
)
from app.usecases.fast_quote.get_all_cooling_load_fast_coefficient import (
    GetAllCoolingLoadFastCoefficienUseCase,
)
from app.usecases.fast_quote.update_cooling_load_fast_coefficient import (
    UpdateCoolingLoadFastCoefficientUseCase,
)
from app.usecases.humid_air.get_full_ha_props import GetFullHAPropertyUseCase
from app.usecases.user.get_all_users import GetAllUsersUsecase
from app.usecases.user.login_user import LoginUserUseCase
from app.usecases.user.register_user import UserSignUpUseCase
from infra.data.repositories.fast_quote_sqlrepo import (
    ColdRoomCoolingCoefficientSQLRepository,
)
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
            "infra.web.api.v1.routes.protected_routes",
            "infra.web.api.v1.routes.fast_quote_routes",
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

    # TODO : Créer des dictionnaires, exemple :
    #     book_usecases = {
    #     "create": providers.Factory(CreateBookUseCase, repository=book_repository),
    #     "get_all": providers.Factory(GetAllBooksUseCase, repository=book_repository),
    # }
    # TODO : Et modifier les routes, exemple :
    # use_case: CreateBookUseCase = Provide[AppContainer.book_usecases["create"]],

    # === humid air module ===
    # repositories
    # usecases
    get_full_ha_props_usecase = providers.Factory(GetFullHAPropertyUseCase)

    # === user module ===
    # repositories
    user_repository = providers.Factory(
        UserSQLRepository, unit_of_work=unit_of_work, password_hasher=password_hasher
    )
    # usecases
    register_user_usecase = providers.Factory(
        UserSignUpUseCase,
        repository=user_repository,
    )
    login_user_usecase = providers.Factory(
        LoginUserUseCase,
        repository=user_repository,
        password_hasher=password_hasher,
        token_service=token_service,
    )
    get_all_users_usecase = providers.Factory(
        GetAllUsersUsecase, repository=user_repository
    )
    # === fast quote module ===
    # repository
    cold_room_cooling_coef_repository = providers.Factory(
        ColdRoomCoolingCoefficientSQLRepository, unit_of_work=unit_of_work
    )
    # usecases
    add_cooling_load_fast_coefficient_usecase = providers.Factory(
        AddCoolingLoadFastCoefficientUseCase,
        repository=cold_room_cooling_coef_repository,
    )
    update_cooling_load_fast_coefficient_usecase = providers.Factory(
        UpdateCoolingLoadFastCoefficientUseCase,
        repository=cold_room_cooling_coef_repository,
    )
    get_all_cooling_load_fast_coefficients_usecase = providers.Factory(
        GetAllCoolingLoadFastCoefficienUseCase,
        repository=cold_room_cooling_coef_repository,
    )
    calculate_cold_room_cooling_load_fast_usecase = providers.Factory(
        CalculateColdRoomCoolingLoadFastUseCase,
        repository=cold_room_cooling_coef_repository,
    )
