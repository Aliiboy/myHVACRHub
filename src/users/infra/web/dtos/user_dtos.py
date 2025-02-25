from datetime import datetime
from http import HTTPStatus
from uuid import UUID

from flask import Response, jsonify, make_response
from pydantic import BaseModel, EmailStr, Field

from users.domain.entities.user_entity import UserRole
from users.domain.settings.user_settings import UserSettings

# === requests ===


class UserSignUpRequest(BaseModel):
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
    email: EmailStr = Field(..., description=UserSettings.email_description)
    password: str = Field(..., description=UserSettings.password_description)


class GetAllUsersQueryParams(BaseModel):
    limit: int = Field(
        default=100, gt=0, description="Nombre maximum d'utimisateurs à recuperer"
    )


class UserPath(BaseModel):
    id: UUID = Field(..., description="identificant unique de l'utilisateur")


# === responses ===


class UserLoginResponse(BaseModel):
    access_token: str = Field(..., description=UserSettings.access_token_description)

    def to_response(self) -> Response:
        return make_response(jsonify(self.model_dump()), HTTPStatus.OK)


class GetUserResponse(BaseModel):
    id: UUID = Field(..., description=UserSettings.id_description)
    email: EmailStr = Field(..., description=UserSettings.email_description)
    role: UserRole = Field(..., description=UserSettings.role_description)
    created_at: datetime = Field(..., description=UserSettings.created_at_description)

    def to_response(self) -> Response:
        return make_response(jsonify(self.model_dump()), HTTPStatus.OK)


class GetAllUsersResponse(BaseModel):
    users: list[GetUserResponse] = Field(..., description="Liste des utilisateurs")

    def to_response(self) -> Response:
        return make_response(jsonify(self.model_dump()), HTTPStatus.OK)
