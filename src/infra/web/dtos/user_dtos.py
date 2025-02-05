import re
from typing import Any

from pydantic import BaseModel, EmailStr, Field, model_validator

from domain.settings.user_settings import UserSettings


class RegisterRequestDTO(BaseModel):
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

        if not isinstance(password, str):
            # TODO : Personnaliser les erreurs
            raise ValueError("Le mot de passe doit être une chaîne de caractères.")

        if not (re.search(r"\d", password) and re.search(r"[@$!%*?&]", password)):
            # TODO : Personnaliser les erreurs
            raise ValueError(
                "Le mot de passe doit contenir au moins un chiffre et un caractère spécial."
            )

        return value


class LoginRequestDTO(BaseModel):
    email: EmailStr = Field(..., description=UserSettings.email_description)
    password: str = Field(..., description=UserSettings.password_description)


class TokenResponseDTO(BaseModel):
    access_token: str = Field(..., description=UserSettings.access_token_description)
    token_type: str = Field(
        default="Bearer", description=UserSettings.token_type_description
    )
