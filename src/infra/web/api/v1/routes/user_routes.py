from collections.abc import Callable
from typing import cast

from dependency_injector.wiring import Provide, inject
from flask import Response, jsonify, make_response
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_openapi3 import APIBlueprint, Tag  # type: ignore[attr-defined]

from app.usecases.user.authenticate_user import AuthenticateUserUseCase
from app.usecases.user.create_user import CreateUserUseCase
from infra.web.container import AppContainer
from infra.web.dtos.common import ErrorResponse
from infra.web.dtos.user_dtos import (
    LoginRequestDTO,
    RegisterRequestDTO,
    TokenResponseDTO,
)

tag = Tag(name="Authentication", description="Routes pour l'authentification")


router = APIBlueprint(
    "/auth",
    __name__,
    url_prefix="/auth",
    abp_tags=[tag],
    abp_responses={"422": ErrorResponse, "500": ErrorResponse},
    doc_ui=True,
)


@router.post("/register", responses={201: TokenResponseDTO, 400: ErrorResponse})
@inject
def register(
    body: RegisterRequestDTO,
    use_case: CreateUserUseCase = Provide[AppContainer.create_user_usecase],
) -> Response:
    try:
        use_case.execute(email=body.email, password=body.password)
        return make_response(jsonify({"message": "Utilisateur créé avec succès"}), 201)
    except ValueError as e:
        error_response = ErrorResponse(code=400, message=str(e))
        return make_response(jsonify(error_response.model_dump()), 400)


@router.post("/login", responses={200: TokenResponseDTO})
@inject
def login(
    body: LoginRequestDTO,
    use_case: AuthenticateUserUseCase = Provide[AppContainer.authenticate_user_usecase],
) -> Response:
    try:
        token = use_case.execute(email=body.email, password=body.password)
        return make_response(
            jsonify({"access_token": token, "token_type": "Bearer"}), 200
        )
    except ValueError as e:
        error_response = ErrorResponse(code=401, message=str(e))
        return make_response(jsonify(error_response.model_dump()), 401)


@router.get("/protected")
@cast("Callable[..., Response]", jwt_required())
def protected_route() -> Response:
    current_user = get_jwt_identity()
    return make_response(jsonify({"message": f"Bienvenue, {current_user}"}), 200)
