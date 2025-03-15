from datetime import datetime
from http import HTTPStatus
from uuid import UUID

from flask import Response, jsonify, make_response
from pydantic import BaseModel, EmailStr, Field

from users.domain.entities.user_entity import UserRole
from users.domain.settings.user_settings import UserSettings

# === requests ===


class UserSignUpRequest(BaseModel):
    """Schéma de validation d'un nouvel utilisateur

    Args:
        BaseModel (BaseModel): Schéma de validation d'un nouvel utilisateur
    """

    email: EmailStr = Field(
        ...,
        description=UserSettings.email_description,
    )
    password: str = Field(
        ...,
        description=UserSettings.password_description,
        min_length=UserSettings.password_min_length,
        pattern=UserSettings.password_pattern,
    )


class UserLoginRequest(BaseModel):
    """Schéma de validation d'un utilisateur à connecter

    Args:
        BaseModel (BaseModel): Schéma de validation d'un utilisateur à connecter
    """

    email: EmailStr = Field(..., description=UserSettings.email_description)
    password: str = Field(..., description=UserSettings.password_description)


class GetAllUsersQueryParams(BaseModel):
    """Schéma de validation des paramètres de la requête

    Args:
        BaseModel (BaseModel): Schéma de validation des paramètres de la requête
    """

    limit: int = Field(
        default=UserSettings.limit_default,
        gt=UserSettings.limit_gt,
        description=UserSettings.limit_description,
    )


class UserPath(BaseModel):
    """Schéma de validation du chemin de l'utilisateur

    Args:
        BaseModel (BaseModel): Schéma de validation du chemin de l'utilisateur
    """

    id: UUID = Field(..., description=UserSettings.user_id_description)


# === responses ===


class UserLoginResponse(BaseModel):
    """Schéma de validation de la réponse de connexion d'un utilisateur

    Args:
        BaseModel (BaseModel): Schéma de validation de la réponse de connexion d'un utilisateur

    Returns:
        str: Jeton d'accès
    """

    access_token: str = Field(..., description=UserSettings.access_token_description)

    def to_response(self) -> Response:
        return make_response(jsonify(self.model_dump()), HTTPStatus.OK)


class GetUserResponse(BaseModel):
    """Schéma de validation de la réponse d'un utilisateur

    Args:
        BaseModel (BaseModel): Schéma de validation de la réponse d'un utilisateur

    Returns:
        dict: Profil utilisateur
    """

    id: UUID = Field(..., description=UserSettings.user_id_description)
    email: EmailStr = Field(..., description=UserSettings.email_description)
    role: UserRole = Field(..., description=UserSettings.role_description)
    created_at: datetime = Field(..., description=UserSettings.created_at_description)
    updated_at: datetime = Field(..., description=UserSettings.updated_at_description)

    def to_response(self) -> Response:
        return make_response(jsonify(self.model_dump()), HTTPStatus.OK)


class GetAllUsersResponse(BaseModel):
    """Schéma de validation de la réponse de la liste des utilisateurs

    Args:
        BaseModel (BaseModel): Schéma de validation de la réponse de la liste des utilisateurs

    Returns:
        list[GetUserResponse]: Liste des utilisateurs
    """

    users: list[GetUserResponse] = Field(
        ..., description=UserSettings.users_description
    )

    def to_response(self) -> Response:
        return make_response(jsonify(self.model_dump()), HTTPStatus.OK)
