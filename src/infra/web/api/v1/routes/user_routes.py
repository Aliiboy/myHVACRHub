from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from flask import Response
from flask_openapi3 import APIBlueprint, Tag  # type: ignore[attr-defined]

from app.usecases.user.authenticate_user import AuthenticateUserUseCase
from app.usecases.user.create_user import CreateUserUseCase
from domain.exceptions.user_exceptions import (
    UserAlreadyExistsException,
    UserInvalidPasswordException,
    UserNotFoundException,
)
from infra.web.container import AppContainer
from infra.web.dtos.generic import ClientErrorResponse, SuccessResponse
from infra.web.dtos.user_dtos import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
)

tag = Tag(name="Authentication", description="S'enregistrer et se connecter à l'API")


router = APIBlueprint(
    "/auth",
    __name__,
    url_prefix="/auth",
    abp_tags=[tag],
    doc_ui=True,
)


@router.post(
    "/register",
    description="Permet de s'enregistrer dans la base de données de l'API",
    responses={
        HTTPStatus.CREATED: SuccessResponse,
        HTTPStatus.CONFLICT: ClientErrorResponse,
    },
)
@inject
def register(
    body: RegisterRequest,
    use_case: CreateUserUseCase = Provide[AppContainer.create_user_usecase],
) -> Response:
    try:
        use_case.execute(email=body.email, password=body.password)
        return SuccessResponse(
            code=HTTPStatus.CREATED, message="Utilisateur créé avec succès"
        ).to_response()

    except UserAlreadyExistsException as e:
        return ClientErrorResponse(
            code=HTTPStatus.CONFLICT, message=str(e)
        ).to_response()


@router.post(
    "/login",
    description="Permet de se connecter et de récuperer le token pour l'inserer dans votre agent GPT",
    responses={
        HTTPStatus.OK: LoginResponse,
        HTTPStatus.NOT_FOUND: ClientErrorResponse,
        HTTPStatus.UNAUTHORIZED: ClientErrorResponse,
    },
)
@inject
def login(
    body: LoginRequest,
    use_case: AuthenticateUserUseCase = Provide[AppContainer.authenticate_user_usecase],
) -> Response:
    try:
        token = use_case.execute(email=body.email, password=body.password)
        return LoginResponse(access_token=token).to_response()

    except UserNotFoundException as e:
        return ClientErrorResponse(
            code=HTTPStatus.NOT_FOUND, message=str(e)
        ).to_response()

    except UserInvalidPasswordException as e:
        return ClientErrorResponse(
            code=HTTPStatus.UNAUTHORIZED, message=str(e)
        ).to_response()
