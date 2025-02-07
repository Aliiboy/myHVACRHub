import re
from http import HTTPStatus
from typing import Any

from flask import Response, jsonify, make_response
from pydantic import BaseModel, EmailStr, Field, model_validator

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
