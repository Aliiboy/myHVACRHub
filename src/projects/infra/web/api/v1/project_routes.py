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
from projects.app.schemas.project_schema import (
    ProjectAddMemberSchema,
    ProjectCreateSchema,
    ProjectUpdateSchema,
)
from projects.app.usecases.add_project_member import AddProjectMemberUseCase
from projects.app.usecases.create_project import CreateProjectUseCase
from projects.app.usecases.delete_project import DeleteProjectUseCase
from projects.app.usecases.delete_project_member import DeleteProjectMemberUseCase
from projects.app.usecases.get_all_projects import GetAllProjectsUseCase
from projects.app.usecases.get_project_by_id import GetProjectByIdUseCase
from projects.app.usecases.get_project_members import GetProjectMembersUseCase
from projects.app.usecases.get_user_projects import GetUserProjectsUseCase
from projects.app.usecases.update_project import UpdateProjectUseCase
from projects.domain.exceptions.project_exceptions import (
    ProjectDBException,
    ProjectMemberValidationException,
    ProjectValidationException,
)
from projects.infra.web.dtos.project_dtos import (
    GetAllProjectsQueryParams,
    GetAllProjectsResponse,
    GetProjectMembersResponse,
    GetProjectResponse,
    GetUserResponse,
    ProjectAddMemberRequest,
    ProjectCreateRequest,
    ProjectMemberPath,
    ProjectPath,
    ProjectUpdateRequest,
)
from users.domain.entities.user_entity import UserRole
from users.infra.web.decorators.role_required import role_required

tag = Tag(name="Projects", description="Gestion des projets et de leurs membres")

security = [{"jwt": []}]  # type: ignore[var-annotated]

router = APIBlueprint(
    "/projects",
    __name__,
    url_prefix="/projects",
    abp_tags=[tag],
    doc_ui=True,
)


@router.post(
    "/create_project",
    description="Permet de créer un nouveau projet.",
    security=security,
    responses={
        HTTPStatus.CREATED: SuccessResponse,
        HTTPStatus.UNPROCESSABLE_ENTITY: ErrorResponse,
    },
)
@inject
@cast("Callable[..., Response]", jwt_required())
def create_project(
    body: ProjectCreateRequest,
    use_case: CreateProjectUseCase = Provide[
        AppContainer.project_usecases.provided["create_project"]
    ],
) -> Response:
    """Permet de créer un nouveau projet.

    Args:
        body (ProjectCreateRequest): Schéma de validation d'un nouveau projet
        use_case (CreateProjectUseCase, optional): Cas d'utilisation pour créer un nouveau projet.

    Returns:
        Response: Réponse de succès ou d'erreur
    """
    try:
        schema = ProjectCreateSchema(
            project_number=body.project_number,
            name=body.name,
            description=body.description,
        )
        user_id = UUID(get_jwt().get("sub"))
        use_case.execute(schema=schema, creator_id=user_id)
        return SuccessResponse(
            code=HTTPStatus.CREATED, message="Projet créé avec succès."
        ).to_response()

    except ProjectValidationException as e:
        return ErrorResponse(
            code=HTTPStatus.UNPROCESSABLE_ENTITY, message=e.errors
        ).to_response()

    except ProjectDBException as e:
        return ErrorResponse(
            code=HTTPStatus.UNPROCESSABLE_ENTITY, message=str(e)
        ).to_response()


@router.get(
    "get_all_projects",
    description="Permet de récupérer la liste de tous les projets.",
    security=security,
    responses={
        HTTPStatus.OK: GetAllProjectsResponse,
    },
)
@inject
@cast("Callable[..., Response]", jwt_required())
@cast("Callable[..., Response]", role_required(UserRole.ADMIN))
def get_all_projects(
    query: GetAllProjectsQueryParams,
    use_case: GetAllProjectsUseCase = Provide[
        AppContainer.project_usecases.provided["get_all_projects"]
    ],
) -> Response:
    """Permet de récupérer la liste de tous les projets.

    Args:
        query (GetAllProjectsQueryParams): Paramètres de requête
        use_case (GetAllProjectsUseCase, optional): Cas d'utilisation pour récupérer tous les projets.

    Returns:
        Response: Réponse de succès ou d'erreur
    """
    projects = use_case.execute(limit=query.limit)
    projects_response = [
        GetProjectResponse.model_validate(project.model_dump()) for project in projects
    ]
    return GetAllProjectsResponse(projects=projects_response).to_response()


@router.get(
    "/<uuid:id>",
    description="Permet de récupérer un projet par son identifiant.",
    security=security,
    responses={
        HTTPStatus.OK: GetProjectResponse,
        HTTPStatus.NOT_FOUND: ErrorResponse,
    },
)
@inject
@cast("Callable[..., Response]", jwt_required())
def get_project_by_id(
    path: ProjectPath,
    use_case: GetProjectByIdUseCase = Provide[
        AppContainer.project_usecases.provided["get_project_by_id"]
    ],
) -> Response:
    """Permet de récupérer un projet par son identifiant.

    Args:
        path (ProjectPath): Chemin avec l'identifiant du projet
        use_case (GetProjectByIdUseCase, optional): Cas d'utilisation pour récupérer un projet par son identifiant.

    Returns:
        Response: Réponse de succès ou d'erreur
    """
    try:
        project = use_case.execute(path.id)
        return GetProjectResponse.model_validate(project.model_dump()).to_response()

    except ProjectDBException as e:
        return ErrorResponse(code=HTTPStatus.NOT_FOUND, message=str(e)).to_response()


@router.put(
    "/<uuid:id>",
    description="Permet de mettre à jour un projet existant.",
    security=security,
    responses={
        HTTPStatus.OK: GetProjectResponse,
        HTTPStatus.NOT_FOUND: ErrorResponse,
        HTTPStatus.UNPROCESSABLE_ENTITY: ErrorResponse,
    },
)
@inject
@cast("Callable[..., Response]", jwt_required())
def update_project(
    path: ProjectPath,
    body: ProjectUpdateRequest,
    use_case: UpdateProjectUseCase = Provide[
        AppContainer.project_usecases.provided["update_project"]
    ],
) -> Response:
    """Permet de mettre à jour un projet existant.

    Args:
        path (ProjectPath): Chemin avec l'identifiant du projet
        body (ProjectUpdateRequest): Schéma de validation pour la mise à jour d'un projet
        use_case (UpdateProjectUseCase, optional): Cas d'utilisation pour mettre à jour un projet.

    Returns:
        Response: Réponse de succès ou d'erreur
    """
    try:
        schema = ProjectUpdateSchema(
            id=path.id,
            project_number=body.project_number,
            name=body.name,
            description=body.description,
        )
        updated_project = use_case.execute(schema=schema)
        return GetProjectResponse.model_validate(
            updated_project.model_dump()
        ).to_response()

    except ProjectValidationException as e:
        return ErrorResponse(
            code=HTTPStatus.UNPROCESSABLE_ENTITY, message=e.errors
        ).to_response()

    except ProjectDBException as e:
        return ErrorResponse(code=HTTPStatus.NOT_FOUND, message=str(e)).to_response()


@router.delete(
    "/<uuid:id>",
    description="Permet de supprimer un projet existant.",
    security=security,
    responses={
        HTTPStatus.OK: SuccessResponse,
        HTTPStatus.NOT_FOUND: ErrorResponse,
    },
)
@inject
@cast("Callable[..., Response]", jwt_required())
def delete_project(
    path: ProjectPath,
    use_case: DeleteProjectUseCase = Provide[
        AppContainer.project_usecases.provided["delete_project"]
    ],
) -> Response:
    """Permet de supprimer un projet existant.

    Args:
        path (ProjectPath): Chemin avec l'identifiant du projet
        use_case (DeleteProjectUseCase, optional): Cas d'utilisation pour supprimer un projet.

    Returns:
        Response: Réponse de succès ou d'erreur
    """
    try:
        use_case.execute(project_id=path.id)
        return SuccessResponse(
            code=HTTPStatus.OK, message="Projet supprimé avec succès."
        ).to_response()

    except ProjectDBException as e:
        return ErrorResponse(code=HTTPStatus.NOT_FOUND, message=str(e)).to_response()


@router.post(
    "/<uuid:id>/members",
    description="Permet d'ajouter un membre à un projet.",
    security=security,
    responses={
        HTTPStatus.CREATED: SuccessResponse,
        HTTPStatus.NOT_FOUND: ErrorResponse,
        HTTPStatus.UNPROCESSABLE_ENTITY: ErrorResponse,
    },
)
@inject
@cast("Callable[..., Response]", jwt_required())
def add_project_member(
    path: ProjectPath,
    body: ProjectAddMemberRequest,
    use_case: AddProjectMemberUseCase = Provide[
        AppContainer.project_usecases.provided["add_project_member"]
    ],
) -> Response:
    """Permet d'ajouter un membre à un projet.

    Args:
        path (ProjectPath): Chemin de la requête
        body (ProjectAddMemberRequest): Corps de la requête
        use_case (AddProjectMemberUseCase, optional): Cas d'utilisation pour ajouter un membre à un projet.

    Returns:
        Response: Réponse de succès ou d'erreur
    """
    try:
        schema = ProjectAddMemberSchema(
            project_id=path.id,
            user_id=body.user_id,
        )
        use_case.execute(schema=schema)
        return SuccessResponse(
            code=HTTPStatus.CREATED, message="Membre ajouté au projet avec succès."
        ).to_response()

    except ProjectMemberValidationException as e:
        return ErrorResponse(
            code=HTTPStatus.UNPROCESSABLE_ENTITY, message=e.errors
        ).to_response()

    except ProjectDBException as e:
        return ErrorResponse(code=HTTPStatus.NOT_FOUND, message=str(e)).to_response()


@router.delete(
    "/<uuid:project_id>/members/<uuid:user_id>",
    description="Permet de supprimer un membre d'un projet.",
    security=security,
    responses={
        HTTPStatus.OK: SuccessResponse,
        HTTPStatus.NOT_FOUND: ErrorResponse,
    },
)
@inject
@cast("Callable[..., Response]", jwt_required())
def delete_project_member(
    path: ProjectMemberPath,
    use_case: DeleteProjectMemberUseCase = Provide[
        AppContainer.project_usecases.provided["delete_project_member"]
    ],
) -> Response:
    """Permet de supprimer un membre d'un projet.

    Args:
        path (ProjectMemberPath): Chemin avec l'identifiant du projet et de l'utilisateur
        use_case (DeleteProjectMemberUseCase, optional): Cas d'utilisation pour supprimer un membre d'un projet.

    Returns:
        Response: Réponse de succès ou d'erreur
    """
    try:
        use_case.execute(project_id=path.project_id, user_id=path.user_id)
        return SuccessResponse(
            code=HTTPStatus.OK, message="Membre supprimé du projet avec succès."
        ).to_response()

    except ProjectDBException as e:
        return ErrorResponse(code=HTTPStatus.NOT_FOUND, message=str(e)).to_response()


@router.get(
    "/<uuid:id>/members",
    description="Permet de récupérer tous les membres d'un projet.",
    security=security,
    responses={
        HTTPStatus.OK: GetProjectMembersResponse,
        HTTPStatus.NOT_FOUND: ErrorResponse,
    },
)
@inject
@cast("Callable[..., Response]", jwt_required())
def get_project_members(
    path: ProjectPath,
    use_case: GetProjectMembersUseCase = Provide[
        AppContainer.project_usecases.provided["get_project_members"]
    ],
) -> Response:
    """Permet de récupérer tous les membres d'un projet.

    Args:
        path (ProjectPath): Chemin avec l'identifiant du projet
        use_case (GetProjectMembersUseCase, optional): Cas d'utilisation pour récupérer les membres d'un projet.

    Returns:
        Response: Réponse de succès ou d'erreur
    """
    try:
        members = use_case.execute(project_id=path.id)
        members_response = [
            GetUserResponse(id=member.id, email=member.email, role=member.role.value)
            for member in members
        ]
        return GetProjectMembersResponse(members=members_response).to_response()

    except ProjectDBException as e:
        return ErrorResponse(code=HTTPStatus.NOT_FOUND, message=str(e)).to_response()


@router.get(
    "/user/projects",
    description="Permet de récupérer tous les projets de l'utilisateur connecté.",
    security=security,
    responses={
        HTTPStatus.OK: GetAllProjectsResponse,
        HTTPStatus.NOT_FOUND: ErrorResponse,
    },
)
@inject
@cast("Callable[..., Response]", jwt_required())
def get_user_projects(
    use_case: GetUserProjectsUseCase = Provide[
        AppContainer.project_usecases.provided["get_user_projects"]
    ],
) -> Response:
    """Permet de récupérer tous les projets de l'utilisateur connecté.

    Args:
        use_case (GetUserProjectsUseCase, optional): Cas d'utilisation pour récupérer les projets d'un utilisateur.

    Returns:
        Response: Réponse de succès ou d'erreur
    """
    try:
        user_id = UUID(get_jwt().get("sub"))
        projects = use_case.execute(user_id=user_id)
        projects_response = [
            GetProjectResponse.model_validate(project.model_dump())
            for project in projects
        ]
        return GetAllProjectsResponse(projects=projects_response).to_response()

    except ProjectDBException as e:
        return ErrorResponse(code=HTTPStatus.NOT_FOUND, message=str(e)).to_response()
