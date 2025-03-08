from datetime import datetime
from uuid import UUID

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

from projects.infra.data.models.project_sqlmodel import (
    ProjectAndUserJonctionTableSQLModel,
    ProjectSQLModel,
)
from users.domain.entities.user_entity import UserEntity, UserRole


class UserSQLModel(SQLModel, table=True):
    """Utilisateur

    Représente un utilisateur avec son email, son mot de passe et son rôle.

    Attributs:
        id (UUID): Identifiant unique pour l'utilisateur
        email (EmailStr): Email de l'utilisateur
        password (str): Mot de passe de l'utilisateur
        role (UserRole): Rôle de l'utilisateur
        created_at (datetime): Date de création de l'utilisateur
        updated_at (datetime): Date de mise à jour de l'utilisateur
    """

    __tablename__ = "users"

    id: UUID = Field(..., primary_key=True)
    email: EmailStr = Field(..., unique=True, index=True)
    password: str = Field(...)
    role: UserRole = Field(...)
    created_at: datetime = Field(
        ...,
    )
    updated_at: datetime = Field(
        ...,
    )
    projects: list[ProjectSQLModel] = Relationship(
        back_populates="members", link_model=ProjectAndUserJonctionTableSQLModel
    )

    def to_entity(self, include_related: bool = True) -> UserEntity:
        """Convertit le modèle SQL en entité

        Args:
            include_related (bool, optional): Indique si les relations doivent être incluses. Defaults to True.

        Returns:
            UserEntity: Entité utilisateur
        """
        return UserEntity(
            id=self.id,
            email=self.email,
            password=self.password,
            role=self.role,
            created_at=self.created_at,
            updated_at=self.updated_at,
            projects=[
                project.to_entity(include_related=False) for project in self.projects
            ]
            if include_related
            else [],
        )
