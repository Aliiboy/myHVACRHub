from datetime import datetime, timezone
from enum import Enum
from typing import ForwardRef
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field

from users.domain.settings.user_settings import UserSettings

# Référence avancée pour ProjectEntity
ProjectEntityRef = ForwardRef("ProjectEntity")


class UserRole(str, Enum):
    """Rôle de l'utilisateur

    Enum représentant les rôles possibles pour les utilisateurs.

    Attributs:
        ADMIN (str): Rôle administrateur
        MODERATOR (str): Rôle modérateur
        USER (str): Rôle utilisateur
    """

    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"
    USER = "USER"


class UserEntity(BaseModel):
    """Utilisateur

    Représente un utilisateur avec son email, son mot de passe et son rôle.

    Attributs:
        id (UUID): Identifiant unique pour l'utilisateur
        email (EmailStr): Email de l'utilisateur
        password (str): Mot de passe de l'utilisateur
        role (UserRole): Rôle de l'utilisateur
        created_at (datetime): Date de création de l'utilisateur
        updated_at (datetime): Date de mise à jour de l'utilisateur
        projects (list[ProjectEntityRef]): Liste des projets de l'utilisateur
    """

    id: UUID = Field(default_factory=uuid4)
    email: EmailStr = Field(
        ...,
    )
    password: str = Field(
        ...,
        min_length=UserSettings.password_min_length,
        pattern=UserSettings.password_pattern,
    )
    role: UserRole = Field(default=UserRole.USER)
    created_at: datetime = Field(default=datetime.now(timezone.utc))
    updated_at: datetime = Field(default=datetime.now(timezone.utc))
    projects: list[ProjectEntityRef] = Field(default_factory=list)  # type: ignore
