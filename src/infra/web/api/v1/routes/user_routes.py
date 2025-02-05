from dependency_injector.wiring import Provide, inject
from flask import Response, jsonify, make_response
from flask_openapi3 import APIBlueprint, Tag
from networkx import descendants  # type: ignore[attr-defined]

from app.usecases.user.authenticate_user import AuthenticateUserUseCase
from app.usecases.user.create_user import CreateUserUseCase
from infra.web.container import AppContainer
from infra.web.dtos.common import ErrorResponse
from infra.web.dtos.user_dtos import (
    LoginRequestDTO,
    RegisterRequestDTO,
    TokenResponseDTO,
)

tag = Tag(name="Authentication", description="S'enregistrer et se connecter à l'API")


router = APIBlueprint(
    "/auth",
    __name__,
    url_prefix="/auth",
    abp_tags=[tag],
    abp_responses={"401": ErrorResponse, "422": ErrorResponse, "500": ErrorResponse},
    doc_ui=True,
)


@router.post("/register",
             description="Permet de s'enregistrer dans la base de données de l'API"
             responses={201: TokenResponseDTO, 400: ErrorResponse})
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


@router.post("/login",
             description="Permet de se connecter et de récuperer le token pour l'inserer dans votre agent GPT",
             responses={200: TokenResponseDTO})
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
