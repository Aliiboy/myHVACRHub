from collections.abc import Callable
from http import HTTPStatus
from typing import cast
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from flask import Response
from flask_jwt_extended import get_jwt, jwt_required
from flask_openapi3 import APIBlueprint, Tag  # type: ignore[attr-defined]

from common.infra.web.container import AppContainer
from common.infra.web.dtos.generic import ErrorResponse, SuccessResponse
from users.app.schemas.user_schema import UserLoginSchema, UserSignUpSchema
from users.app.usecases.delete_user import DeleteUserByIdUsecase
from users.app.usecases.get_all_users import GetAllUsersUsecase
from users.app.usecases.get_user_profile import GetUserProfileUseCase
from users.app.usecases.login_user import UserLoginUseCase
from users.app.usecases.sign_up_user import UserSignUpUseCase
from users.domain.entities.user_entity import UserRole
from users.domain.exceptions.user_exceptions import (
    UserDBException,
    UserValidationException,
)
from users.infra.web.decorators.role_required import role_required
from users.infra.web.dtos.user_dtos import (
    GetAllUsersQueryParams,
    GetAllUsersResponse,
    GetUserResponse,
    UserLoginRequest,
    UserLoginResponse,
    UserPath,
    UserSignUpRequest,
)

tag = Tag(name="Authentication", description="S'enregistrer et se connecter à l'API")

security = [{"jwt": []}]  # type: ignore[var-annotated]

router = APIBlueprint(
    "/auth",
    __name__,
    url_prefix="/auth",
    abp_tags=[tag],
    doc_ui=True,
)


@router.post(
    "/sign_up",
    description="Permet de s'enregistrer dans la base de données de l'API.",
    responses={
        HTTPStatus.CREATED: SuccessResponse,
        HTTPStatus.UNPROCESSABLE_ENTITY: ErrorResponse,
    },
)
@inject
def sign_up(
    body: UserSignUpRequest,
    use_case: UserSignUpUseCase = Provide[
        AppContainer.user_usecases.provided["sign_up"]
    ],
) -> Response:
    """Permet de s'enregistrer dans la base de données de l'API.

    Args:
        body (UserSignUpRequest): Schéma de validation d'un nouvel utilisateur
        use_case (UserSignUpUseCase, optional): Cas d'utilisation pour enregistrer un nouvel utilisateur. Defaults to Provide[ AppContainer.user_usecases.provided["sign_up"] ].

    Returns:
        Response: Réponse de succès ou d'erreur
    """
    try:
        schema = UserSignUpSchema(email=body.email, password=body.password)
        use_case.execute(schema=schema)
        return SuccessResponse(
            code=HTTPStatus.CREATED, message="Utilisateur créé avec succès."
        ).to_response()

    except UserValidationException as e:
        return ErrorResponse(
            code=HTTPStatus.UNPROCESSABLE_ENTITY, message=e.errors
        ).to_response()

    except UserDBException as e:
        return ErrorResponse(
            code=HTTPStatus.UNPROCESSABLE_ENTITY, message=str(e)
        ).to_response()


@router.delete(
    "/user/<uuid:id>",
    description="Permet de supprimer un utilisateur de la base de données de l'API.",
    security=security,
    responses={
        HTTPStatus.OK: SuccessResponse,
        HTTPStatus.NOT_FOUND: ErrorResponse,
        HTTPStatus.FORBIDDEN: ErrorResponse,
    },
)
@inject
@cast("Callable[..., Response]", jwt_required())
@cast("Callable[..., Response]", role_required(UserRole.ADMIN))
def delete_user_by_id(
    path: UserPath,
    use_case: DeleteUserByIdUsecase = Provide[
        AppContainer.user_usecases.provided["delete_user"]
    ],
) -> Response:
    """Permet de supprimer un utilisateur de la base de données de l'API.

    Args:
        path (UserPath): Chemin de l'utilisateur à supprimer
        use_case (DeleteUserByIdUsecase, optional): Cas d'utilisation pour supprimer un utilisateur par son identifiant. Defaults to Provide[ AppContainer.user_usecases.provided["delete_user"] ].

    Returns:
        Response: Réponse de succès ou d'erreur
    """
    try:
        use_case.execute(user_id=path.id)
        return SuccessResponse(
            code=HTTPStatus.OK, message="Utilisateur supprimé avec succès."
        ).to_response()

    except UserDBException as e:
        return ErrorResponse(code=HTTPStatus.NOT_FOUND, message=str(e)).to_response()


@router.post(
    "/login",
    description="Permet de se connecter et de récuperer le token.",
    responses={
        HTTPStatus.OK: UserLoginResponse,
        HTTPStatus.UNPROCESSABLE_ENTITY: ErrorResponse,
    },
)
@inject
def login(
    body: UserLoginRequest,
    use_case: UserLoginUseCase = Provide[AppContainer.user_usecases.provided["login"]],
) -> Response:
    """Permet de se connecter et de récuperer le token.

    Args:
        body (UserLoginRequest): Schéma de validation d'un utilisateur à connecter
        use_case (UserLoginUseCase, optional): Cas d'utilisation pour se connecter et de récuperer le token. Defaults to Provide[AppContainer.user_usecases.provided["login"]].

    Returns:
        Response: Réponse de succès ou d'erreur
    """
    try:
        schema = UserLoginSchema(email=body.email, password=body.password)
        token = use_case.execute(schema=schema)
        return UserLoginResponse(access_token=token).to_response()

    except UserValidationException as e:
        return ErrorResponse(
            code=HTTPStatus.UNPROCESSABLE_ENTITY, message=e.errors
        ).to_response()

    except UserDBException as e:
        return ErrorResponse(
            code=HTTPStatus.UNPROCESSABLE_ENTITY, message=str(e)
        ).to_response()


@router.get(
    "/profile",
    description="Permet de voir son profil utilisateur.",
    security=security,
    responses={
        HTTPStatus.OK: GetUserResponse,
        HTTPStatus.NOT_FOUND: ErrorResponse,
    },
)
@inject
@cast("Callable[..., Response]", jwt_required())
def get_user_profile(
    use_case: GetUserProfileUseCase = Provide[
        AppContainer.user_usecases.provided["get_user_profile"]
    ],
) -> Response:
    """Permet de voir son profil utilisateur.

    Args:
        use_case (GetUserProfileUseCase, optional): Cas d'utilisation pour voir son profil utilisateur. Defaults to Provide[ AppContainer.user_usecases.provided["get_user_profile"] ].

    Returns:
        Response: Réponse de succès ou d'erreur
    """
    user_id = UUID(get_jwt().get("sub"))
    try:
        user = use_case.execute(user_id=user_id)
        return GetUserResponse.model_validate(user.model_dump()).to_response()

    except UserDBException as e:
        return ErrorResponse(code=HTTPStatus.NOT_FOUND, message=str(e)).to_response()


@router.get(
    "get_all_users",
    description="Récupère la liste de tous les utilisateurs",
    security=security,
    responses={
        HTTPStatus.OK: GetAllUsersResponse,
        HTTPStatus.FORBIDDEN: ErrorResponse,
    },
)
@cast("Callable[..., Response]", jwt_required())
@cast("Callable[..., Response]", role_required(UserRole.ADMIN))
@inject
def get_all_users(
    query: GetAllUsersQueryParams,
    use_case: GetAllUsersUsecase = Provide[
        AppContainer.user_usecases.provided["get_all_users"]
    ],
) -> Response:
    """Récupère la liste de tous les utilisateurs.

    Args:
        query (GetAllUsersQueryParams): Schéma de validation des paramètres de la requête
        use_case (GetAllUsersUsecase, optional): Cas d'utilisation pour récupérer la liste de tous les utilisateurs. Defaults to Provide[ AppContainer.user_usecases.provided["get_all_users"] ].

    Returns:
        Response: Réponse de succès ou d'erreur
    """
    users = use_case.execute(limit=query.limit)
    users_to = [GetUserResponse.model_validate(user.model_dump()) for user in users]
    return GetAllUsersResponse(users=users_to).to_response()
