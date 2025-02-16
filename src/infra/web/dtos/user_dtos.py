from datetime import datetime
from http import HTTPStatus
from uuid import UUID

from flask import Response, jsonify, make_response
from pydantic import BaseModel, EmailStr, Field

from domain.entities.user.user_entity import UserRole
from domain.settings.user_settings import UserSettings


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description=UserSettings.email_description)
    password: str = Field(..., description=UserSettings.password_description)


class LoginResponse(BaseModel):
    access_token: str = Field(..., description=UserSettings.access_token_description)

    def to_response(self) -> Response:
        return make_response(jsonify(self.model_dump()), HTTPStatus.OK)


class UserResponse(BaseModel):
    id: UUID = Field(..., description=UserSettings.id_description)
    email: EmailStr = Field(..., description=UserSettings.email_description)
    role: UserRole = Field(..., description=UserSettings.role_description)
    created_at: datetime = Field(..., description=UserSettings.created_at_description)


class GetAllUsersResponse(BaseModel):
    users: list[UserResponse] = Field(..., description="Liste des utilisateurs")

    def to_response(self) -> Response:
        return make_response(jsonify(self.model_dump()), HTTPStatus.OK)


class GetAllUsersQueryParams(BaseModel):
    limit: int = Field(
        default=100, gt=0, description="Nombre maximum d'utimisateurs à recuperer"
    )
