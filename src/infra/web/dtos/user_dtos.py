import re
from datetime import datetime
from http import HTTPStatus
from typing import Any
from uuid import UUID

from flask import Response, jsonify, make_response
from pydantic import BaseModel, EmailStr, Field, model_validator

from domain.entities.user.user_entity import UserRole
from domain.exceptions.user_exceptions import UserInvalidPasswordPatternException
from domain.settings.user_settings import UserSettings


class RegisterRequest(BaseModel):
    email: EmailStr = Field(..., description=UserSettings.email_description)
    password: str = Field(
        ...,
        min_length=UserSettings.password_min_length,
        pattern=UserSettings.password_pattern,
        description=UserSettings.password_description,
    )

    @model_validator(mode="before")
    @classmethod
    def check_password(cls, value: dict[str, Any]) -> dict[str, Any]:
        password = value.get("password", "")

        if not (re.search(r"\d", password) and re.search(r"[@$!%*?&]", password)):
            raise UserInvalidPasswordPatternException()

        return value


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
