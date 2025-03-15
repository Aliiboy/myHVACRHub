from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import ForwardRef
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

from projects.domain.settings.project_settings import ProjectSettings

# Référence avancée pour UserEntity
UserEntityRef = ForwardRef("UserEntity")


class ProjectMemberRole(Enum):
    """Rôle des membres du projet

    Enum représentant les rôles possibles pour les membres d'un projet.

    Attributs:
        ADMIN (str): Rôle administrateur
        MEMBER (str): Rôle membre
    """

    ADMIN = "ADMIN"
    MEMBER = "MEMBER"


class ProjectEntity(BaseModel):
    """Entité projet

    Représente un projet avec ses propriétaires et ses membres.

    Attributs:
        id (UUID): Identifiant unique pour le projet
        project_number (str): Numéro de projet utilisé comme identifiant par l'entreprise
        name (str): Nom du projet
        description (str): Description du projet
        created_at (datetime): Date de création du projet
        updated_at (datetime): Date de mise à jour du projet
        members (list[UserEntity]): Liste des membres du projet
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: UUID = Field(default_factory=uuid4)
    project_number: str = Field(
        ...,
        max_length=ProjectSettings.project_number_max_length,
    )
    name: str = Field(
        ...,
        max_length=ProjectSettings.name_max_length,
    )
    description: str = Field(
        ...,
        max_length=ProjectSettings.description_max_length,
    )
    created_at: datetime = Field(default=datetime.now(timezone.utc))
    updated_at: datetime = Field(default=datetime.now(timezone.utc))
    members: list[UserEntityRef] = Field(default_factory=list)  # type: ignore


class ProjectAndUserJonctionTableEntity(BaseModel):
    """Entité membre du projet

    Représente la table de jointure entre les projets et les utilisateurs, stockant le rôle de chaque utilisateur dans un projet.

    Attributs:
        project_id (UUID): ID du projet associé
        user_id (UUID): ID de l'utilisateur associé
        role (ProjectMemberRole): Rôle de l'utilisateur dans le projet
    """

    project_id: UUID
    user_id: UUID
    role: ProjectMemberRole = Field(default=ProjectMemberRole.MEMBER)
