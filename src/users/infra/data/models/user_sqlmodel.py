from datetime import datetime
from uuid import UUID

from pydantic import EmailStr
from sqlmodel import Field, SQLModel

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

    def to_entity(self) -> UserEntity:
        return UserEntity(
            id=self.id,
            email=self.email,
            password=self.password,
            role=self.role,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
