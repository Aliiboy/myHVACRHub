from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from projects.domain.entities.project_entity import (
    ProjectAndUserJonctionTableEntity,
    ProjectEntity,
    ProjectMemberRole,
)

if TYPE_CHECKING:  # pragma: no cover
    from users.infra.data.models.user_sqlmodel import UserSQLModel


class ProjectAndUserJonctionTableSQLModel(SQLModel, table=True):
    """Modèle SQL pour les membres du projet

    Représente la table de jointure entre les projets et les utilisateurs, stockant le rôle de chaque utilisateur dans un projet.

    Attributs:
        project_id (UUID): ID du projet associé
        user_id (UUID): ID de l'utilisateur associé
        role (ProjectMemberRole): Rôle de l'utilisateur dans le projet
    """

    __tablename__ = "project_members_links"
    project_id: UUID = Field(..., foreign_key="projects.id", primary_key=True)
    user_id: UUID = Field(..., foreign_key="users.id", primary_key=True)
    role: str = Field(...)

    def to_entity(self) -> ProjectAndUserJonctionTableEntity:
        """Convertit le modèle SQL en entité

        Returns:
            ProjectAndUserJonctionTableEntity: Entité membre du projet
        """
        return ProjectAndUserJonctionTableEntity(
            project_id=self.project_id,
            user_id=self.user_id,
            role=ProjectMemberRole(self.role),
        )


class ProjectSQLModel(SQLModel, table=True):
    """Modèle SQL pour les projets

    Représente la structure de table pour les projets dans la base de données.

    Attributs:
        id (UUID): Identifiant unique pour le projet
        project_number (str): Numéro de projet utilisé comme identifiant par l'entreprise
        name (str): Nom du projet
        description (str): Description du projet
        created_at (datetime): Date de création du projet
        updated_at (datetime): Date de mise à jour du projet
        members (list[UserSQLModel]): Liste des membres du projet
    """

    __tablename__ = "projects"
    id: UUID = Field(..., primary_key=True)
    project_number: str = Field(..., unique=True)
    name: str = Field(..., unique=True)
    description: str = Field(...)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)
    members: list["UserSQLModel"] = Relationship(
        back_populates="projects", link_model=ProjectAndUserJonctionTableSQLModel
    )

    def to_entity(self, include_related: bool = True) -> ProjectEntity:
        """Convertit le modèle SQL en entité

        Args:
            include_related (bool, optional): Indique si les relations doivent être incluses. Defaults to True.

        Returns:
            ProjectEntity: Entité projet
        """
        return ProjectEntity(
            id=self.id,
            project_number=self.project_number,
            name=self.name,
            description=self.description,
            created_at=self.created_at,
            updated_at=self.updated_at,
            members=[member.to_entity(include_related=False) for member in self.members]
            if include_related
            else [],
        )
