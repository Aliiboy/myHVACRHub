from datetime import datetime
from http import HTTPStatus
from uuid import UUID

from flask import Response, jsonify, make_response
from pydantic import BaseModel, Field

from projects.domain.settings.project_settings import ProjectSettings

# === requests ===


class ProjectCreateRequest(BaseModel):
    """Schéma de validation pour créer un nouveau projet

    Args:
        BaseModel (BaseModel): Schéma de validation pour créer un nouveau projet
    """

    project_number: str = Field(
        ...,
        max_length=ProjectSettings.project_number_max_length,
        description="Numéro du projet utilisé comme identifiant par l'entreprise",
    )
    name: str = Field(
        ...,
        max_length=ProjectSettings.name_max_length,
        description="Nom du projet",
    )
    description: str = Field(
        ...,
        max_length=ProjectSettings.description_max_length,
        description="Description du projet",
    )


class ProjectUpdateRequest(BaseModel):
    """Schéma de validation pour mettre à jour un projet existant

    Args:
        BaseModel (BaseModel): Schéma de validation pour mettre à jour un projet existant
    """

    project_number: str = Field(
        ...,
        max_length=ProjectSettings.project_number_max_length,
        description="Numéro du projet utilisé comme identifiant par l'entreprise",
    )
    name: str = Field(
        ...,
        max_length=ProjectSettings.name_max_length,
        description="Nom du projet",
    )
    description: str = Field(
        ...,
        max_length=ProjectSettings.description_max_length,
        description="Description du projet",
    )


class ProjectPath(BaseModel):
    """Schéma de validation du chemin pour un projet

    Args:
        BaseModel (BaseModel): Schéma de validation du chemin pour un projet
    """

    id: UUID = Field(..., description="Identifiant unique du projet")


class GetAllProjectsQueryParams(BaseModel):
    """Schéma de validation des paramètres de requête pour récupérer tous les projets

    Args:
        BaseModel (BaseModel): Schéma de validation des paramètres de requête
    """

    limit: int = Field(
        default=100, gt=0, description="Nombre maximum de projets à récupérer"
    )


class ProjectMemberRequest(BaseModel):
    """Schéma de validation pour ajouter un membre à un projet

    Args:
        BaseModel (BaseModel): Schéma de validation pour ajouter un membre à un projet
    """

    user_id: UUID = Field(..., description="Identifiant unique de l'utilisateur")


class ProjectMemberPath(BaseModel):
    """Schéma de validation du chemin pour un membre de projet

    Args:
        BaseModel (BaseModel): Schéma de validation du chemin pour un membre de projet
    """

    project_id: UUID = Field(..., description="Identifiant unique du projet")
    user_id: UUID = Field(..., description="Identifiant unique de l'utilisateur")


# === responses ===


class GetProjectResponse(BaseModel):
    """Schéma de validation de la réponse pour un projet

    Args:
        BaseModel (BaseModel): Schéma de validation de la réponse pour un projet

    Returns:
        dict: Détails du projet
    """

    id: UUID = Field(..., description="Identifiant unique du projet")
    project_number: str = Field(
        ..., description="Numéro du projet utilisé comme identifiant par l'entreprise"
    )
    name: str = Field(..., description="Nom du projet")
    description: str = Field(..., description="Description du projet")
    created_at: datetime = Field(..., description="Date de création du projet")
    updated_at: datetime = Field(
        ..., description="Date de dernière mise à jour du projet"
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

    projects: list[GetProjectResponse] = Field(..., description="Liste des projets")

    def to_response(self) -> Response:
        return make_response(jsonify(self.model_dump()), HTTPStatus.OK)


class GetUserResponse(BaseModel):
    """Schéma de validation de la réponse pour un utilisateur

    Args:
        BaseModel (BaseModel): Schéma de validation de la réponse pour un utilisateur

    Returns:
        dict: Détails de l'utilisateur
    """

    id: UUID = Field(..., description="Identifiant unique de l'utilisateur")
    email: str = Field(..., description="Adresse email de l'utilisateur")
    role: str = Field(..., description="Rôle de l'utilisateur dans le système")

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
        ..., description="Liste des membres du projet"
    )

    def to_response(self) -> Response:
        return make_response(jsonify(self.model_dump()), HTTPStatus.OK)
