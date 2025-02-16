from pydantic import BaseModel, Field

from domain.settings.user_settings import UserSettings


class UserSignUpSchema(BaseModel):
    email: str = Field(
        ...,
        description=UserSettings.email_description,
    )
    password: str = Field(..., description=UserSettings.password_description)
