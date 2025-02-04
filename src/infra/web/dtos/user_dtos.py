from pydantic import BaseModel, EmailStr, Field

from domain.settings.user_settings import UserSettings


class RegisterRequestDTO(BaseModel):
    email: EmailStr = Field(..., description=UserSettings.email_description)
    password: str = Field(
        ...,
        min_length=UserSettings.password_min_length,
        max_length=UserSettings.password_max_length,
        description=UserSettings.password_description,
    )


class LoginRequestDTO(BaseModel):
    email: EmailStr = Field(..., description=UserSettings.email_description)
    password: str = Field(..., description=UserSettings.password_description)


class TokenResponseDTO(BaseModel):
    access_token: str = Field(..., description=UserSettings.access_token_description)
    token_type: str = Field(
        default="Bearer", description=UserSettings.token_type_description
    )
