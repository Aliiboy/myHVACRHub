from collections.abc import Callable
from http import HTTPStatus
from typing import cast

from dependency_injector.wiring import Provide, inject
from flask import Response
from flask_jwt_extended import jwt_required
from flask_openapi3 import APIBlueprint, Tag  # type: ignore[attr-defined]

from common.infra.web.container import AppContainer
from common.infra.web.dtos.generic import ClientErrorResponse, SuccessResponse
from users.app.schemas.user_schema import UserLoginSchema, UserSignUpSchema
from users.app.usecases.delete_user import DeleteUserByIdUsecase
from users.app.usecases.get_all_users import GetAllUsersUsecase
from users.app.usecases.login_user import UserLoginUseCase
from users.app.usecases.sign_up_user import UserSignUpUseCase
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
        HTTPStatus.UNPROCESSABLE_ENTITY: ClientErrorResponse,
    },
)
@inject
def sign_up(
    body: UserSignUpRequest,
    use_case: UserSignUpUseCase = Provide[
        AppContainer.user_usecases.provided["sign_up"]
    ],
) -> Response:
    try:
        request = UserSignUpSchema(email=body.email, password=body.password)
        use_case.execute(request)
        return SuccessResponse(
            code=HTTPStatus.CREATED, message="Utilisateur créé avec succès."
        ).to_response()

    except UserDBException as e:
        return ClientErrorResponse(
            code=HTTPStatus.UNPROCESSABLE_ENTITY, message=str(e)
        ).to_response()


@router.delete(
    "/user/<uuid:id>",
    description="Permet de supprimer un utilisateur de la base de données de l'API.",
    security=security,
    responses={
        HTTPStatus.OK: SuccessResponse,
        HTTPStatus.NOT_FOUND: ClientErrorResponse,
        HTTPStatus.FORBIDDEN: ClientErrorResponse,
    },
)
@inject
@cast("Callable[..., Response]", jwt_required())
@cast("Callable[..., Response]", role_required("admin"))
def delete_user_by_id(
    path: UserPath,
    use_case: DeleteUserByIdUsecase = Provide[
        AppContainer.user_usecases.provided["delete_user"]
    ],
) -> Response:
    try:
        use_case.execute(path.id)
        return SuccessResponse(
            code=HTTPStatus.OK, message="Utilisateur supprimé avec succès."
        ).to_response()

    except UserDBException as e:
        return ClientErrorResponse(
            code=HTTPStatus.NOT_FOUND, message=str(e)
        ).to_response()


@router.post(
    "/login",
    description="Permet de se connecter et de récuperer le token.",
    responses={
        HTTPStatus.OK: UserLoginResponse,
        HTTPStatus.UNPROCESSABLE_ENTITY: ClientErrorResponse,
    },
)
@inject
def login(
    body: UserLoginRequest,
    use_case: UserLoginUseCase = Provide[AppContainer.user_usecases.provided["login"]],
) -> Response:
    try:
        request = UserLoginSchema(email=body.email, password=body.password)
        token = use_case.execute(request)
        return UserLoginResponse(access_token=token).to_response()

    except UserValidationException as e:
        return ClientErrorResponse(
            code=HTTPStatus.UNPROCESSABLE_ENTITY, message=e.errors
        ).to_response()

    except UserDBException as e:
        return ClientErrorResponse(
            code=HTTPStatus.UNPROCESSABLE_ENTITY, message=str(e)
        ).to_response()


@router.get(
    "get_all_users",
    description="Récupère la liste de tous les utilisateurs",
    security=security,
    responses={
        HTTPStatus.OK: GetAllUsersResponse,
        HTTPStatus.FORBIDDEN: ClientErrorResponse,
    },
)
@cast("Callable[..., Response]", jwt_required())
@cast("Callable[..., Response]", role_required("admin"))
@inject
def get_all_users(
    query: GetAllUsersQueryParams,
    use_case: GetAllUsersUsecase = Provide[
        AppContainer.user_usecases.provided["get_all_users"]
    ],
) -> Response:
    users = use_case.execute(limit=query.limit)
    users_to = [GetUserResponse.model_validate(user.model_dump()) for user in users]
    return GetAllUsersResponse(users=users_to).to_response()
