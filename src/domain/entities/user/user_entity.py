from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field

from domain.settings.user_settings import UserSettings


class UserRole(str, Enum):
    admin = "admin"
    moderator = "moderator"
    user = "user"


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4, description=UserSettings.id_description)

    email: EmailStr = Field(..., description=UserSettings.email_description)

    hashed_password: str = Field(
        ...,
        description=UserSettings.password_description,
    )

    # TODO : description dans usersetting
    role: UserRole = Field(default=UserRole.user, description="Rôle de l'utilisateur")

    created_at: datetime = Field(
        default_factory=datetime.utcnow, description=UserSettings.created_at_description
    )
