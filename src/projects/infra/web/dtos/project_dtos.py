from datetime import datetime
from http import HTTPStatus
from uuid import UUID

from flask import Response, jsonify, make_response
from pydantic import BaseModel, Field

from projects.domain.entities.project_entity import ProjectMemberRole
from projects.domain.settings.project_settings import (
    ProjectMemberSettings,
    ProjectSettings,
)

# === requests ===


class ProjectCreateRequest(BaseModel):
    """Schéma de validation pour créer un nouveau projet

    Args:
        BaseModel (BaseModel): Schéma de validation pour créer un nouveau projet
    """

    project_number: str = Field(
        ...,
        max_length=ProjectSettings.project_number_max_length,
        description=ProjectSettings.project_number_description,
    )
    name: str = Field(
        ...,
        max_length=ProjectSettings.name_max_length,
        description=ProjectSettings.name_description,
    )
    description: str = Field(
        ...,
        max_length=ProjectSettings.description_max_length,
        description=ProjectSettings.description_description,
    )


class ProjectUpdateRequest(BaseModel):
    """Schéma de validation pour mettre à jour un projet existant

    Args:
        BaseModel (BaseModel): Schéma de validation pour mettre à jour un projet existant
    """

    project_number: str = Field(
        ...,
        max_length=ProjectSettings.project_number_max_length,
        description=ProjectSettings.project_number_description,
    )
    name: str = Field(
        ...,
        max_length=ProjectSettings.name_max_length,
        description=ProjectSettings.name_description,
    )
    description: str = Field(
        ...,
        max_length=ProjectSettings.description_max_length,
        description=ProjectSettings.description_description,
    )


class ProjectPath(BaseModel):
    """Schéma de validation du chemin pour un projet

    Args:
        BaseModel (BaseModel): Schéma de validation du chemin pour un projet
    """

    id: UUID = Field(..., description=ProjectSettings.project_id_description)


class GetAllProjectsQueryParams(BaseModel):
    """Schéma de validation des paramètres de requête pour récupérer tous les projets

    Args:
        BaseModel (BaseModel): Schéma de validation des paramètres de requête
    """

    limit: int = Field(
        default=ProjectSettings.limit_default,
        gt=ProjectSettings.limit_gt,
        description=ProjectSettings.limit_description,
    )


class ProjectAddMemberRequest(BaseModel):
    """Schéma de validation pour ajouter un membre à un projet

    Args:
        BaseModel (BaseModel): Schéma de validation pour ajouter un membre à un projet
    """

    user_id: UUID = Field(..., description=ProjectMemberSettings.user_id_description)
    role: ProjectMemberRole = Field(
        ..., description=ProjectMemberSettings.role_description
    )


class ProjectMemberPath(BaseModel):
    """Schéma de validation du chemin pour un membre de projet

    Args:
        BaseModel (BaseModel): Schéma de validation du chemin pour un membre de projet
    """

    project_id: UUID = Field(..., description=ProjectSettings.project_id_description)
    user_id: UUID = Field(..., description=ProjectMemberSettings.user_id_description)


# === responses ===


class GetProjectResponse(BaseModel):
    """Schéma de validation de la réponse pour un projet

    Args:
        BaseModel (BaseModel): Schéma de validation de la réponse pour un projet

    Returns:
        dict: Détails du projet
    """

    id: UUID = Field(..., description=ProjectSettings.project_id_description)
    project_number: str = Field(
        ..., description=ProjectSettings.project_number_description
    )
    name: str = Field(..., description=ProjectSettings.name_description)
    description: str = Field(..., description=ProjectSettings.description_description)
    created_at: datetime = Field(
        ..., description=ProjectSettings.created_at_description
    )
    updated_at: datetime = Field(
        ..., description=ProjectSettings.updated_at_description
    )

    def to_response(self) -> Response:
        return make_response(jsonify(self.model_dump()), HTTPStatus.OK)


class GetAllProjectsResponse(BaseModel):
    """Schéma de validation de la réponse pour la liste des projets

    Args:
        BaseModel (BaseModel): Schéma de validation de la réponse pour la liste des projets

    Returns:
        list[GetProjectResponse]: Liste des projets
    """

    projects: list[GetProjectResponse] = Field(
        ..., description=ProjectSettings.projects_description
    )

    def to_response(self) -> Response:
        return make_response(jsonify(self.model_dump()), HTTPStatus.OK)


class GetUserResponse(BaseModel):
    """Schéma de validation de la réponse pour un utilisateur

    Args:
        BaseModel (BaseModel): Schéma de validation de la réponse pour un utilisateur

    Returns:
        dict: Détails de l'utilisateur
    """

    id: UUID = Field(..., description=ProjectMemberSettings.user_id_description)
    email: str = Field(..., description=ProjectMemberSettings.email_description)
    role: str = Field(..., description=ProjectMemberSettings.role_description)

    def to_response(self) -> Response:
        return make_response(jsonify(self.model_dump()), HTTPStatus.OK)


class GetProjectMembersResponse(BaseModel):
    """Schéma de validation de la réponse pour la liste des membres d'un projet

    Args:
        BaseModel (BaseModel): Schéma de validation de la réponse pour la liste des membres

    Returns:
        list[GetUserResponse]: Liste des membres du projet
    """

    members: list[GetUserResponse] = Field(
        ..., description=ProjectMemberSettings.members_description
    )

    def to_response(self) -> Response:
        return make_response(jsonify(self.model_dump()), HTTPStatus.OK)
